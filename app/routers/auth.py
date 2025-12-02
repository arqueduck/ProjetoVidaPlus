from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.config import ALGORITHM, SECRET_KEY, get_access_token_expires
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.deps import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # verifica se email já existe
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado.",
        )

    hashed_password = get_password_hash(user_in.senha)

    db_user = User(
        nome_completo=user_in.nome_completo,
        email=user_in.email,
        senha_hash=hashed_password,
        tipo=user_in.tipo,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(form_data: LoginRequest, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.email == form_data.email)
        .first()
    )
    if not user or not verify_password(form_data.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )

    access_token_expires = get_access_token_expires()
    access_token = create_access_token(
        data={"sub": str(user.id), "tipo": user.tipo},
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token)
