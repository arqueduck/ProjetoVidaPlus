from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ConsultaBase(BaseModel):
    paciente_id: int
    profissional_id: int
    unidade_id: int
    data_hora: datetime
    tipo_atendimento: str  # "PRESENCIAL" ou "TELEMEDICINA"
    observacoes: str | None = None


class ConsultaCreate(ConsultaBase):
    pass


class ConsultaRead(BaseModel):
    id: int
    paciente_id: int
    profissional_id: int
    unidade_id: int
    data_hora: datetime
    tipo_atendimento: str
    status: str
    observacoes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ConsultaUpdate(BaseModel):
    paciente_id: int | None = None
    profissional_id: int | None = None
    unidade_id: int | None = None
    data_hora: datetime | None = None
    tipo_atendimento: str | None = None
    observacoes: str | None = None


class ConsultaStatusUpdate(BaseModel):
    status: str
