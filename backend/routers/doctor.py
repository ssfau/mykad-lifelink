# external imports
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

# local imports
from backend.db import get_db
from backend.main import require_role
from backend.core.ocrmodule import ocr_mykad_image
import backend.schemas as schemas

router = APIRouter()