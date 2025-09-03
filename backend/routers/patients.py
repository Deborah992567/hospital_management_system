from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..auth import require_role, get_current_user

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=schemas.PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(p_in: schemas.PatientCreate, db: Session = Depends(get_db), _=Depends(require_role("receptionist", "admin"))):
    p = models.Patient(**p_in.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/", response_model=list[schemas.PatientOut])
def list_patients(db: Session = Depends(get_db), _=Depends(require_role("admin", "receptionist", "doctor", "nurse"))):
    return db.query(models.Patient).all()

@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db), _=Depends(require_role("admin", "receptionist", "doctor", "nurse"))):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return p

@router.put("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(patient_id: int, p_in: schemas.PatientCreate, db: Session = Depends(get_db), _=Depends(require_role("receptionist", "admin"))):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    for k, v in p_in.dict(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    p = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(p)
    db.commit()
    return None
