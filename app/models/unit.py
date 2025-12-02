from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo_unidade = Column(String, nullable=False)   # HOSPITAL, CLINICA, LABORATORIO, HOMECARE
    endereco = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    profissionais = relationship(
        "Profissional",
        back_populates="unidade",
        cascade="all, delete-orphan",
    )