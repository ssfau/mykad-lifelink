import re
import os
import sys
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from fastapi import FastAPI, UploadFile, File, HTTPException

# Auto-detect Tesseract installation on Windows/Linux
def configure_tesseract():
    """Automatically configure Tesseract path if not in system PATH"""
    # First, check if tesseract is already accessible (e.g., in PATH on Linux)
    try:
        version = pytesseract.get_tesseract_version()
        print(f"Tesseract found in PATH: version {version}")
        return True
    except Exception as e:
        print(f"Tesseract not found in PATH: {e}")
        pass  # Not found, try common paths
    
    # Platform-specific paths
    if sys.platform.startswith('win'):
        # Windows installation paths
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe",
        ]
    else:
        # Linux/Unix paths (Railway uses Linux)
        # Also check if it's in PATH via which command
        import shutil
        tesseract_path = shutil.which('tesseract')
        if tesseract_path:
            print(f"Found tesseract via which: {tesseract_path}")
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            try:
                version = pytesseract.get_tesseract_version()
                print(f"Tesseract configured: version {version}")
                return True
            except Exception:
                pass
        
        common_paths = [
            "/usr/bin/tesseract",
            "/usr/local/bin/tesseract",
            "/bin/tesseract",
        ]
    
    # Try common installation paths
    for path in common_paths:
        if os.path.exists(path):
            print(f"Trying tesseract path: {path}")
            pytesseract.pytesseract.tesseract_cmd = path
            try:
                version = pytesseract.get_tesseract_version()
                print(f"Tesseract configured successfully: {path}, version {version}")
                return True
            except Exception as e:
                print(f"Failed to use {path}: {e}")
                continue  # Try next path
    
    # If we get here, Tesseract is not found
    print("WARNING: Tesseract not found in common paths. OCR may not work.")
    return False

# Configure Tesseract on module import
tesseract_configured = configure_tesseract()

# Manual configuration fallback (mainly for Windows)
if not hasattr(pytesseract.pytesseract, 'tesseract_cmd') or not pytesseract.pytesseract.tesseract_cmd:
    if sys.platform.startswith('win'):
        default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        if os.path.exists(default_path):
            pytesseract.pytesseract.tesseract_cmd = default_path
            print(f"Using Windows default path: {default_path}")
    # On Linux, if still not configured, try one more time with which
    else:
        import shutil
        tesseract_path = shutil.which('tesseract')
        if tesseract_path and not pytesseract.pytesseract.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            print(f"Using tesseract from PATH: {tesseract_path}")

""" HELPER FUNCTIONS """

def looks_like_address(line: str) -> bool:
    address_keywords = [
        "JALAN", "LORONG", "TAMAN", "KAMPUNG",
        "KG", "NO", "BANDAR", "POSKOD", "SELANGOR",
        "KUALA", "MELAKA", "JOHOR", "PULAU", "SABAH", "SARAWAK"
    ]

    if any(char.isdigit() for char in line):
        return True

    return any(word in line for word in address_keywords)


# string splitters based off ocr capture
def extract_nric(text: str):
    """Extract NRIC from OCR text. Malaysian NRIC format: YYMMDD-PB-G####"""
    # Try multiple patterns to find NRIC
    patterns = [
        r'\b\d{6}[- ]?\d{2}[- ]?\d{4}\b',  # Standard format with optional dashes/spaces
        r'\d{6}\s*\d{2}\s*\d{4}',  # With spaces
        r'\d{6}-\d{2}-\d{4}',  # With dashes
        r'\d{12}',  # 12 digits in a row
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # Use the first match that looks like an NRIC
            for match in matches:
                # Extract just digits
                raw = re.sub(r'\D', '', match)
                # Check if it's 12 digits (valid NRIC length)
                if len(raw) == 12:
                    return f"{raw[:6]}-{raw[6:8]}-{raw[8:]}"
                # Also accept 11 digits (might be missing last digit due to OCR error)
                elif len(raw) == 11:
                    return f"{raw[:6]}-{raw[6:8]}-{raw[8:]}0"  # Add trailing 0
                # Or 10 digits
                elif len(raw) == 10:
                    return f"{raw[:6]}-{raw[6:8]}-{raw[8:]}00"
    
    return None


def extract_name(text: str):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines_upper = [line.upper() for line in lines]

    # Step 1: Find NRIC line index
    nric_index = None
    for i, line in enumerate(lines_upper):
        if re.search(r'\d{6}[- ]?\d{2}[- ]?\d{4}', line):
            nric_index = i
            break

    if nric_index is None:
        return None

    # Step 2: Name is usually right after NRIC
    for i in range(nric_index + 1, min(nric_index + 4, len(lines_upper))):
        candidate = lines_upper[i]

        # Must be uppercase letters + spaces
        if not re.fullmatch(r"[A-Z @'.\-]+", candidate):
            continue

        # Must not be address
        if looks_like_address(candidate):
            continue

        # Reasonable name length
        if len(candidate) < 5:
            continue

        return candidate

    return None

""" IMAGE PROCESSING OCR """

# image selection + processing
def process_image_bytes(image_bytes: bytes):
    """Process image for better OCR accuracy"""
    img = Image.open(BytesIO(image_bytes))
    
    # Convert to RGB if necessary (PIL requires RGB for some operations)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    print(f"Opened image: {img.format}, Size: {img.size}, Mode: {img.mode}")

    # Convert to grayscale for better OCR
    img = img.convert('L')  # Convert to grayscale
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # Increase contrast by 50%
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)  # Increase sharpness
    
    # Resize if image is too small (OCR works better with larger images)
    width, height = img.size
    min_size = 1000
    if width < min_size or height < min_size:
        scale = min_size / min(width, height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        print(f"Resized image to: {new_width}x{new_height} for better OCR")
    
    # Apply slight denoising
    img = img.filter(ImageFilter.MedianFilter(size=3))
    
    return img


# USE THIS ONLY
async def ocr_mykad_image(file: UploadFile = File(...)):
    try:
        content_type = file.content_type

        if not content_type or not content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type")

        image_bytes = await file.read()
        processed_image = process_image_bytes(image_bytes)

        # Check if Tesseract is accessible before attempting OCR
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            error_msg = (
                "Tesseract OCR is not installed or not found.\n\n"
                "Please install Tesseract OCR:\n"
                "1. Download from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                "2. Install and check 'Add to PATH' during installation\n"
                "3. Restart your terminal and server\n\n"
                "OR manually configure the path in backend/core/ocrmodule.py:\n"
                "pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'\n\n"
                f"Error: {str(e)}"
            )
            raise HTTPException(status_code=500, detail=error_msg)
        
        # Perform OCR with multiple configurations for better accuracy
        ocr_text = None
        ocr_errors = []
        
        # Try different OCR configurations
        configs = [
            '--psm 6',  # Assume uniform block of text
            '--psm 7',  # Treat image as single text line
            '--psm 8',  # Treat image as single word
            '--psm 11', # Sparse text
            '',  # Default
        ]
        
        for config in configs:
            try:
                if config:
                    ocr_text = pytesseract.image_to_string(processed_image, config=config)
                else:
                    ocr_text = pytesseract.image_to_string(processed_image)
                
                # If we got some text, use it
                if ocr_text and len(ocr_text.strip()) > 0:
                    print(f"OCR successful with config: {config if config else 'default'}")
                    break
            except Exception as e:
                ocr_errors.append(f"Config '{config}': {str(e)}")
                continue
        
        # If all configs failed, try one more time with default
        if not ocr_text or len(ocr_text.strip()) == 0:
            try:
                ocr_text = pytesseract.image_to_string(processed_image, lang='eng')
            except Exception as e:
                ocr_errors.append(f"Default with lang='eng': {str(e)}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"OCR processing failed. Errors: {'; '.join(ocr_errors)}"
                )
        
        if not ocr_text or len(ocr_text.strip()) == 0:
            raise HTTPException(
                status_code=500,
                detail="OCR did not extract any text from the image. Please ensure the image is clear and readable."
            )
        
        print(f"OCR extracted text (first 200 chars): {ocr_text[:200]}")
        
        nric = extract_nric(ocr_text)
        name = extract_name(ocr_text)
        
        print(f"Extracted NRIC: {nric}, Name: {name}")

        return {
            "nric": nric,
            "name": name,
            "raw_ocr": ocr_text
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


