import re
import os
from io import BytesIO
from PIL import Image
import pytesseract
from fastapi import FastAPI, UploadFile, File, HTTPException

# Auto-detect Tesseract installation on Windows if not in PATH
def configure_tesseract():
    """Automatically configure Tesseract path if not in system PATH"""
    # Common Windows installation paths
    common_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Tesseract-OCR\tesseract.exe",
    ]
    
    # Check if tesseract is already accessible
    try:
        pytesseract.get_tesseract_version()
        return  # Already working
    except Exception:
        pass  # Not found, try common paths
    
    # Try common installation paths
    for path in common_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            try:
                pytesseract.get_tesseract_version()
                return  # Successfully configured
            except Exception:
                continue  # Try next path
    
    # If we get here, Tesseract is not found

# Configure Tesseract on module import
configure_tesseract()

# Manual configuration: If auto-detection fails, set your Tesseract path here:
# Since Tesseract is installed but not in PATH, set it directly
if not hasattr(pytesseract.pytesseract, 'tesseract_cmd') or not pytesseract.pytesseract.tesseract_cmd:
    default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_path):
        pytesseract.pytesseract.tesseract_cmd = default_path

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
    match = re.search(r'\b\d{6}[- ]?\d{2}[- ]?\d{4}\b', text)
    if not match:
        return None

    # add dashes
    raw = re.sub(r'\D', '', match.group())
    return f"{raw[:6]}-{raw[6:8]}-{raw[8:]}"


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
    img = Image.open(BytesIO(image_bytes))
    print(f"Opened image: {img.format}, Size: {img.size}")

    width, height = img.size
    min_dim = min(width, height)

    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim

    return img.crop((left, top, right, bottom))


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
        
        # Perform OCR
        try:
            ocr_text = pytesseract.image_to_string(processed_image)
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"OCR processing failed: {str(e)}"
            )

        nric = extract_nric(ocr_text)
        name = extract_name(ocr_text)

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


