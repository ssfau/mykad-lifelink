# external imports
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, ForeignKey, JSON
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date, timedelta

# local imports
from backend.db import get_db, Base
import backend.schemas as schemas

""" PATIENT REGISTRATION """

# small data formats

class PreviousMajorSurgeries(Base):
    __tablename__ = "previous_major_surgeries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)

    surgery_name: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="major_surgeries")

class MedicationPrescription(Base):
    __tablename__ = "medication_prescriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)

    prescription_name: Mapped[str] = mapped_column(String, nullable=False)
    prescription_dose: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="prescriptions")

class Immunization(Base):
    __tablename__ = "immunizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)

    immunization_name: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="immunization")

class PresentingComplaint(Base):
    __tablename__ = "presenting_complaints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)

    complaint: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="presenting_complaint")

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)

    name: Mapped[str] = mapped_column(String, nullable=False)
    contact_number: Mapped[str] = mapped_column(String, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=True)
    date_added: Mapped[Date] = mapped_column(Date, nullable=False)
    additional_info: Mapped[str] = mapped_column(String, nullable=True)

    patient: Mapped["Patient"] = relationship("Patient", back_populates="emergency_contacts")


# big table

class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    nric_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    sex: Mapped[str] = mapped_column(String, nullable=False)
    blood_type: Mapped[str] = mapped_column(String, nullable=False)

    allergies: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    chronic_conditions: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    risk_factors: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    advanced_directives: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)

    major_surgeries: Mapped[List["PreviousMajorSurgeries"]] = relationship("PreviousMajorSurgeries", back_populates="patient")
    prescriptions: Mapped[List["MedicationPrescription"]] = relationship("MedicationPrescription", back_populates="patient")
    immunization: Mapped[List["Immunization"]] = relationship("Immunization", back_populates="patient")
    presenting_complaint: Mapped[List["PresentingComplaint"]] = relationship("PresentingComplaint", back_populates="patient")
    emergency_contacts: Mapped[List["EmergencyContact"]] = relationship("EmergencyContact", back_populates="patient")

# non critical data sending

class PatientRegistrationConfirm(BaseModel):
    full_name: str
    birth_date: date
    nric_number: str
    sex: str

    blood_type: str
    allergies: Optional[List[str]] = None
    chronic_conditions: Optional[List[str]] = None
    risk_factors: Optional[List[str]] = None
    emergency_contacts: Optional[List[str]] = None