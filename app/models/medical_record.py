from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Prontuario(Base):
    __tablename__ = "prontuarios"

    id = Column(Integer, primary_key=True, index=True)

    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    profissional_id = Column(Integer, ForeignKey("profissionais.id"), nullable=False)
    consulta_id = Column(Integer, ForeignKey("consultas.id"), nullable=True)

    data_registro = Column(DateTime(timezone=True), server_default=func.now())
    descricao = Column(Text, nullable=False)
    tipo_registro = Column(String, nullable=False)  # EX: "EVOLUCAO", "PRESCRICAO", "ALTA"

    paciente = relationship("Paciente", backref="prontuarios")
    profissional = relationship("Profissional", backref="prontuarios")
    consulta = relationship("Consulta", backref="prontuarios")
