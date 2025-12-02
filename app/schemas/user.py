from typing import Literal
from pydantic import BaseModel, EmailStr


UserType = Literal["PACIENTE", "PROFISSIONAL", "ADMIN"]


class UserBase(BaseModel):
    nome_completo: str
    email: EmailStr
    tipo: UserType


class UserCreate(UserBase):
    senha: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
