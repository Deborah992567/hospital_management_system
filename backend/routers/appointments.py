from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas 
import models
from database import get_db
from auth import require_role, get_current_user
from datetime import datetime

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=schemas.AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(a_in: schemas.AppointmentCreate, db: Session = Depends(get_db), _=Depends(require_role("receptionist", "doctor", "admin"))):
    patient = db.query(models.Patient).filter(models.Patient.id == a_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    doctor = db.query(models.User).filter(models.User.id == a_in.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    appt = models.Appointment(**a_in.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

@router.get("/", response_model=list[schemas.AppointmentOut])
def list_appointments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # doctors only see their own appts unless admin or receptionist
    if current_user.role == "doctor":
        return db.query(models.Appointment).filter(models.Appointment.doctor_id == current_user.id).all()
    return db.query(models.Appointment).all()

@router.put("/{appt_id}", response_model=schemas.AppointmentOut)
def update_appointment(appt_id: int, a_in: schemas.AppointmentCreate, db: Session = Depends(get_db), _=Depends(require_role("receptionist", "doctor", "admin"))):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for k, v in a_in.dict(exclude_unset=True).items():
        setattr(appt, k, v)
    db.commit()
    db.refresh(appt)
    return appt

@router.delete("/{appt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appt_id: int, db: Session = Depends(get_db), _=Depends(require_role("admin", "receptionist"))):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appt)
    db.commit()
    return None
