from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)

    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)

    data_hora = Column(DateTime, nullable=False)
    tipo_atendimento = Column(String, nullable=False)  # "PRESENCIAL" ou "TELEMEDICINA"
    status = Column(String, nullable=False, default="AGENDADA")
    observacoes = Column(Text, nullable=True)

    criada_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizada_em = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    paciente = relationship("Paciente", backref="consultas")
    profissional = relationship("Profissional", backref="consultas")
    unidade = relationship("Unidade", backref="consultas")
