from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..auth import require_role, get_current_user
from datetime import datetime

router = APIRouter(prefix="/lab", tags=["Lab"])

@router.post("/tests", response_model=schemas.LabTestOut, status_code=status.HTTP_201_CREATED)
def create_test(t_in: schemas.LabTestCreate, db: Session = Depends(get_db), _=Depends(require_role("lab_technician", "admin"))):
    existing = db.query(models.LabTest).filter(models.LabTest.name == t_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Lab test already exists")
    t = models.LabTest(**t_in.dict())
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.post("/results", response_model=schemas.LabResultOut, status_code=status.HTTP_201_CREATED)
def create_result(r_in: schemas.LabResultCreate, db: Session = Depends(get_db), _=Depends(require_role("lab_technician", "admin"))):
    patient = db.query(models.Patient).filter(models.Patient.id == r_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    test = db.query(models.LabTest).filter(models.LabTest.id == r_in.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    lr = models.LabResult(patient_id=r_in.patient_id, test_id=r_in.test_id, result=r_in.result, status="completed", date=datetime.utcnow())
    db.add(lr)
    db.commit()
    db.refresh(lr)
    return lr

@router.get("/results", response_model=list[schemas.LabResultOut])
def list_results(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # doctors can view lab results; admin and lab_technician can view all
    if current_user.role == "doctor":
        # doctor sees all results (doctors may need to filter by patient in frontend)
        return db.query(models.LabResult).all()
    return db.query(models.LabResult).all()
