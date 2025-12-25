import re
from io import BytesIO
from PIL import Image
import pytesseract
from fastapi import FastAPI, UploadFile, File, HTTPException

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


