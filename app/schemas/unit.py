from pydantic import BaseModel, ConfigDict


class UnidadeBase(BaseModel):
    nome: str
    tipo_unidade: str
    endereco: str
    telefone: str


class UnidadeCreate(UnidadeBase):
    pass


class UnidadeRead(UnidadeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UnidadeUpdate(BaseModel):
    nome: str | None = None
    tipo_unidade: str | None = None
    endereco: str | None = None
    telefone: str | None = None
