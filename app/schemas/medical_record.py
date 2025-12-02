from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProntuarioBase(BaseModel):
    paciente_id: int
    profissional_id: int
    consulta_id: int | None = None
    descricao: str
    tipo_registro: str  # "EVOLUCAO", "PRESCRICAO", "ALTA", etc.


class ProntuarioCreate(ProntuarioBase):
    pass


class ProntuarioRead(BaseModel):
    id: int
    paciente_id: int
    profissional_id: int
    consulta_id: int | None = None
    data_registro: datetime
    descricao: str
    tipo_registro: str

    model_config = ConfigDict(from_attributes=True)
