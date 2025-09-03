from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import schemas 
import models
from database import get_db
from auth import require_role

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=schemas.DepartmentOut, status_code=status.HTTP_201_CREATED)
def create_department(dep: schemas.DepartmentCreate, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    existing = db.query(models.Department).filter(models.Department.name == dep.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Department already exists")
    d = models.Department(name=dep.name)
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

@router.get("/", response_model=list[schemas.DepartmentOut])
def list_departments(db: Session = Depends(get_db), _=Depends(require_role("admin", "receptionist", "doctor", "nurse", "accountant", "lab_technician"))):
    return db.query(models.Department).all()
