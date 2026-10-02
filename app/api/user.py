from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginRead, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
    ) -> UserRead:
    #ver si el email existe
    existing = db.scalar(select(User).where(User.email == user.email))
    
    if existing is not None:
        raise HTTPException(status_code=409, detail="El email ya esta registrado")
    
    row = User(
        name= user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(row)
    db.commit()
    return UserRead(name=row.name, email=row.email)

@router.post("/login")
def login(
    login: LoginRead,
    db: Session = Depends(get_db)
    ) -> Token:
    row = db.scalar(select(User).where(User.email == login.email))
    if row is None:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not verify_password(login.password, row.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return Token(access_token=create_access_token(row.id))