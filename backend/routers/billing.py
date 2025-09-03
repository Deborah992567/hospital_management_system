from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..auth import require_role, get_current_user
from datetime import datetime

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/", response_model=schemas.BillOut, status_code=status.HTTP_201_CREATED)
def create_bill(b_in: schemas.BillCreate, db: Session = Depends(get_db), _=Depends(require_role("accountant", "admin"))):
    patient = db.query(models.Patient).filter(models.Patient.id == b_in.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    bill = models.Bill(patient_id=b_in.patient_id, amount=b_in.amount, description=b_in.description, paid=False, date=datetime.utcnow())
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill

@router.get("/", response_model=list[schemas.BillOut])
def list_bills(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # accountants and admins see all bills
    if current_user.role in ("accountant", "admin"):
        return db.query(models.Bill).all()
    # other roles (doctors, receptionist) can be restricted; patients aren't staff so not directly supported here
    raise HTTPException(status_code=403, detail="Access denied")
