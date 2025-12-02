from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict


class PacienteBase(BaseModel):
    nome_completo: str
    email: EmailStr
    cpf: str
    data_nascimento: date
    telefone: str
    endereco: str
    plano_saude: str | None = None
    numero_carteirinha: str | None = None


class PacienteCreate(PacienteBase):
    senha: str  # usada para criar o usuário vinculado


class PacienteRead(BaseModel):
    id: int
    usuario_id: int
    nome_completo: str
    email: EmailStr
    cpf: str
    data_nascimento: date
    telefone: str
    endereco: str
    plano_saude: str | None = None
    numero_carteirinha: str | None = None

    model_config = ConfigDict(from_attributes=True)


class PacienteUpdate(BaseModel):
    telefone: str | None = None
    endereco: str | None = None
    plano_saude: str | None = None
    numero_carteirinha: str | None = None
