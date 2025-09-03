from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..auth import require_role, get_password_hash, get_current_user

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_staff(user_in: schemas.UserCreate, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = get_password_hash(user_in.password)
    user = models.User(
        name=user_in.name,
        email=user_in.email,
        password=hashed,
        role=user_in.role,
        department_id=user_in.department_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/", response_model=list[schemas.UserOut])
def list_staff(db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    return db.query(models.User).all()
