# external imports
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta

# local imports
from backend.db import get_db
from backend.auth import require_auth
from backend.core.ocrmodule import ocr_mykad_image
from backend.core import patient_logic
import backend.schemas as schemas

router = APIRouter()

""" DOCTOR VIEWING PATIENT DATA"""

# confirmed by frontend, this is to get data from ic scan and return that text to frontend
@router.post("/doctor/viewpatientdata/mykadscan")
async def ocr_mykadscan(file: UploadFile = File(...), db: Session = Depends(get_db), session=Depends(require_auth(["doctor"]))):
    # reminder: save raw ocr text to database
    return await ocr_mykad_image(file)

# view patient data
@router.get("/doctor/viewpatientdata/profile", response_model=schemas.PatientDataResponse)
def get_patient_profile(nric: str, db: Session = Depends(get_db), session=Depends(require_auth(["doctor"]))):
    # Query patient by NRIC
    patient = db.query(patient_logic.Patient).filter(patient_logic.Patient.nric_number == nric).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    major_surgeries = [
        {"surgery_name": s.surgery_name, "date": s.date, "additional_info": s.additional_info}
        for s in patient.major_surgeries
    ]
    prescriptions = [
        {"prescription_name": p.prescription_name, "prescription_dose": p.prescription_dose, "date": p.date, "additional_info": p.additional_info}
        for p in patient.prescriptions
    ]
    immunization = [
        {"immunization_name": i.immunization_name, "date": i.date, "additional_info": i.additional_info}
        for i in patient.immunization
    ]
    presenting_complaint = [
        {"complaint": c.complaint, "date": c.date, "additional_info": c.additional_info}
        for c in patient.presenting_complaint
    ]
    emergency_contacts = [
        {"name": e.name, "contact_number": e.contact_number, "address": e.address, "date_added": e.date_added, "additional_info": e.additional_info}
        for e in patient.emergency_contacts
    ]

    return {
        "full_name": patient.full_name,
        "birth_date": patient.birth_date,
        "nric_number": patient.nric_number,
        "sex": patient.sex,
        "blood_type": patient.blood_type,
        "allergies": patient.allergies,
        "chronic_conditions": patient.chronic_conditions,
        "major_surgeries": major_surgeries,
        "prescriptions": prescriptions,
        "immunization": immunization,
        "presenting_complaint": presenting_complaint,
        "risk_factors": patient.risk_factors,
        "advanced_directives": patient.advanced_directives,
        "emergency_contacts": emergency_contacts,
    }