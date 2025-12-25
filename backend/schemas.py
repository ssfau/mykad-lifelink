from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional

#################################
###                           ###
###    PATIENT DATA SCHEMA    ###
###                           ###
#################################

# small data formats

class PreviousMajorSurgeries(BaseModel):
    surgery_name: str = Field(..., examples=["kidney transplant"])
    date: date = Field(...)
    additional_info: str = Field(..., examples=["surgery successful at hsaas"])

class MedicationPrescription(BaseModel):
    prescription_name: str = Field(..., examples=["paracetamol 500mg"])
    prescription_dose: str = Field(..., examples=["3x a day after eating"])
    date: date = Field(...)
    additional_info: str = Field(..., examples=["given from clinic ammar"])

class Immunization(BaseModel):
    immunization_name: str = Field(..., examples=["h5n1 vaccine"])
    date: date = Field(...)
    additional_info: str = Field(..., examples=["booster dose"])

class PresentingComplaint(BaseModel):
    complaint: str = Field(..., examples=["h5n1 vaccine"])
    date: date = Field(...)
    additional_info: str = Field(..., examples=["booster dose"])

class EmergencyContact(BaseModel):
    name: str = Field(..., examples=["h5n1 vaccine"])
    contact_number: str = Field(..., examples=["+604102980415921321"])
    address: str = Field(..., examples=["jalan 5 batu bandar seri petaling"])
    date_added: date = Field(...)
    additional_info: str = Field(..., examples=["son", "father"])


# main schemas

class PatientDataBase(BaseModel):
    full_name: str = Field(..., examples=["ALI BIN ABU"]) 
    birth_date: date = Field(...) 
    nric_number: str = Field(..., examples=["061111111111"]) 
    sex: str = Field(..., examples=["male", "female"]) 
    blood_type: str = Field(..., examples=["O-"])

    allergies: list[str] | None = None
    chronic_conditions: list[str] | None = None

    major_surgeries: list[PreviousMajorSurgeries] | None = None
    prescriptions: list[MedicationPrescription] | None = None
    immunization: list[Immunization] | None = None
    presenting_complaint: list[PresentingComplaint] | None = None

    risk_factors: list[str] | None = None
    advanced_directives: list[str] | None = None
    emergency_contacts: list[EmergencyContact] | None = None

class PatientDataCreate(PatientDataBase):
    user_id: str = Field(..., examples=["abc123xyz"])

class PatientDataResponse(PatientDataBase):
    user_id: str = Field(..., examples=["abc123xyz"])

# clinic admin purposes

class ClinicPatientViewResponse(BaseModel):
    full_name: str
    sex: str
    birth_date: date
    nric_number: str

    prescriptions: list[MedicationPrescription] | None = None
    presenting_complaint: list[PresentingComplaint] | None = None

class ClinicPatientUpdateRequest(BaseModel):
    prescriptions: list[MedicationPrescription] | None = None
    presenting_complaint: list[PresentingComplaint] | None = None
