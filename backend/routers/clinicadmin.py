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

""" CLINIC VIEWING PATIENT DATA"""

# confirmed by frontend, this is to get data from ic scan and return that text to frontend
@router.post("/clinicadmin/viewpatientdata/mykadscan")
async def ocr_mykadscan(file: UploadFile = File(...), db: Session = Depends(get_db), session=Depends(require_auth(["clinic_admin"]))):
    # reminder: save raw ocr text to database
    return await ocr_mykad_image(file)

# view patient data limited to their role
@router.get(
    "/clinic/viewpatientdata/profile",
    response_model=schemas.ClinicPatientViewResponse
)
def get_patient_profile_clinic(
    nric: str,
    db: Session = Depends(get_db),
    session=Depends(require_auth(["clinic_admin"]))
):
    patient = (
        db.query(patient_logic.Patient)
        .filter(patient_logic.Patient.nric_number == nric)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    prescriptions = [
        {
            "prescription_name": p.prescription_name,
            "prescription_dose": p.prescription_dose,
            "date": p.date,
            "additional_info": p.additional_info,
        }
        for p in patient.prescriptions
    ]

    presenting_complaint = [
        {
            "complaint": c.complaint,
            "date": c.date,
            "additional_info": c.additional_info,
        }
        for c in patient.presenting_complaint
    ]

    return {
        "full_name": patient.full_name,
        "sex": patient.sex,
        "birth_date": patient.birth_date,
        "nric_number": patient.nric_number,
        "prescriptions": prescriptions,
        "presenting_complaint": presenting_complaint,
    }

# add prescription or complaints
@router.post("/clinic/viewpatientdata/update")
def clinic_add_patient_records(
    nric: str,
    payload: schemas.ClinicPatientUpdateRequest,
    db: Session = Depends(get_db),
    session=Depends(require_auth(["clinic_admin"]))
):
    patient = (
        db.query(patient_logic.Patient)
        .filter(patient_logic.Patient.nric_number == nric)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Add prescriptions
    if payload.prescriptions:
        for p in payload.prescriptions:
            db_prescription = patient_logic.MedicationPrescription(
                prescription_name=p.prescription_name,
                prescription_dose=p.prescription_dose,
                date=p.date,
                additional_info=p.additional_info,
                patient_id=patient.id,
            )
            db.add(db_prescription)

    # Add presenting complaints
    if payload.presenting_complaint:
        for c in payload.presenting_complaint:
            db_complaint = patient_logic.PresentingComplaint(
                complaint=c.complaint,
                date=c.date,
                additional_info=c.additional_info,
                patient_id=patient.id,
            )
            db.add(db_complaint)

    db.commit()

    return {"status": "success", "message": "Patient records updated"}
