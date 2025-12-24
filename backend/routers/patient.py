# external imports
from fastapi import APIRouter, Depends, UploadFile, File
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

# local imports
from backend.db import get_db
from backend.main import require_role
from backend.core.ocrmodule import ocr_mykad_image
import backend.schemas as schemas

router = APIRouter()

""" PATIENT REGISTRATION """
# no token check required

# this is only to save raw ocr text and make sure data read is strictly backend, name and ic confirmation incase of type will be updated later
@router.post("/patient/mykadscan/initial")
async def ocr_mykadscan(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # reminder: save raw ocr text to database
    return await ocr_mykad_image(file)

@router.post("/patient/mykadscan/confirmation")
def confirm_mykadscan(nric: str, name: str, db: Session = Depends(get_db)):
    return "a"