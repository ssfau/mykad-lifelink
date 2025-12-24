import re
from io import BytesIO
from PIL import Image
import pytesseract
from fastapi import FastAPI, UploadFile, File, HTTPException

# string splitters based off ocr capture
def extract_nric(text: str):
    match = re.search(r'\b\d{6}-?\d{2}-?\d{4}\b', text)
    return match.group(0) if match else None

def extract_name(text: str):
    lines = text.splitlines()

    for i, line in enumerate(lines):
        line_upper = line.upper()

        if "NAMA" in line_upper or "NAME" in line_upper:
            # Try next line first
            if i + 1 < len(lines):
                candidate = lines[i + 1].strip()
                if candidate.isupper() and len(candidate) > 3:
                    return candidate

            # Fallback: same line
            parts = line.split(":")
            if len(parts) > 1:
                candidate = parts[-1].strip()
                if candidate.isupper():
                    return candidate

    return None

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
    content_type = file.content_type

    if not content_type or not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    image_bytes = await file.read()
    processed_image = process_image_bytes(image_bytes)

    ocr_text = pytesseract.image_to_string(processed_image)

    nric = extract_nric(ocr_text)
    name = extract_name(ocr_text)

    return {
        "nric": nric,
        "name": name,
        "raw_ocr": ocr_text
    }


