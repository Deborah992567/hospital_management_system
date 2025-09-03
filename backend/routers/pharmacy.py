from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas 
import models
from database import get_db
from auth import require_role, get_current_user

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])

@router.post("/medicines", response_model=schemas.MedicineOut, status_code=status.HTTP_201_CREATED)
def create_medicine(m_in: schemas.MedicineCreate, db: Session = Depends(get_db), _=Depends(require_role("accountant", "admin"))):
    med = models.Medicine(**m_in.dict())
    db.add(med)
    db.commit()
    db.refresh(med)
    return med

@router.get("/medicines", response_model=list[schemas.MedicineOut])
def list_medicines(db: Session = Depends(get_db), _=Depends(require_role("admin", "doctor", "nurse", "accountant", "receptionist"))):
    return db.query(models.Medicine).all()

@router.post("/prescriptions", response_model=schemas.PrescriptionOut, status_code=status.HTTP_201_CREATED)
def create_prescription(p_in: schemas.PrescriptionCreate, db: Session = Depends(get_db), _=Depends(require_role("doctor", "admin"))):
    patient = db.query(models.Patient).filter(models.Patient.id == p_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    med = db.query(models.Medicine).filter(models.Medicine.id == p_in.medicine_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medicine not found")
    pres = models.Prescription(**p_in.dict())
    # optionally decrement stock (kept minimal per requirements; if you want, handle separately)
    db.add(pres)
    db.commit()
    db.refresh(pres)
    return pres
