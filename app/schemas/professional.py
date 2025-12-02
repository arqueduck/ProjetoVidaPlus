from pydantic import BaseModel, EmailStr


class ProfissionalBase(BaseModel):
    nome_completo: str
    email: EmailStr
    cpf: str
    registro_conselho: str
    tipo_conselho: str
    especialidade: str
    unidade_id: int | None = None


class ProfissionalCreate(ProfissionalBase):
    senha: str  # usada para criar o usuário vinculado


class ProfissionalRead(BaseModel):
    id: int
    usuario_id: int
    nome_completo: str
    email: EmailStr
    cpf: str
    registro_conselho: str
    tipo_conselho: str
    especialidade: str
    unidade_id: int | None = None

    class Config:
        orm_mode = True


class ProfissionalUpdate(BaseModel):
    registro_conselho: str | None = None
    tipo_conselho: str | None = None
    especialidade: str | None = None
    unidade_id: int | None = None
