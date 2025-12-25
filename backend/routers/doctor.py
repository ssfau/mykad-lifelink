# external imports
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

# local imports
from backend.db import get_db
from backend.main import require_auth
from backend.core.ocrmodule import ocr_mykad_image
from backend.core import patient_logic
import backend.schemas as schemas

router = APIRouter()