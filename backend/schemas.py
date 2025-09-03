from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- Auth / Users ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # required: admin, doctor, nurse, lab_technician, accountant, receptionist
    department_id: Optional[int] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    department_id: Optional[int]
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Departments ---
class DepartmentCreate(BaseModel):
    name: str

class DepartmentOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

# --- Patients ---
class PatientCreate(BaseModel):
    name: str
    dob: Optional[datetime] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    department_id: Optional[int] = None

class PatientOut(PatientCreate):
    id: int
    class Config:
        orm_mode = True

# --- Appointments ---
class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date_time: datetime
    note: Optional[str] = None

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date_time: datetime
    status: str
    note: Optional[str]
    class Config:
        orm_mode = True

# --- Pharmacy ---
class MedicineCreate(BaseModel):
    name: str
    stock: int
    price: float
    expiry_date: Optional[datetime] = None

class MedicineOut(MedicineCreate):
    id: int
    class Config:
        orm_mode = True

class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    medicine_id: int
    dosage: Optional[str] = None

class PrescriptionOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    medicine_id: int
    dosage: Optional[str]
    date_prescribed: datetime
    class Config:
        orm_mode = True

# --- Lab ---
class LabTestCreate(BaseModel):
    name: str
    description: Optional[str] = None

class LabTestOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        orm_mode = True

class LabResultCreate(BaseModel):
    patient_id: int
    test_id: int
    result: Optional[str] = None

class LabResultOut(BaseModel):
    id: int
    patient_id: int
    test_id: int
    result: Optional[str]
    date: datetime
    status: str
    class Config:
        orm_mode = True

# --- Billing ---
class BillCreate(BaseModel):
    patient_id: int
    amount: float
    description: Optional[str] = None

class BillOut(BillCreate):
    id: int
    paid: bool
    date: datetime
    class Config:
        orm_mode = True
