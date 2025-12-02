from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)

    cpf = Column(String, unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    plano_saude = Column(String, nullable=True)
    numero_carteirinha = Column(String, nullable=True)

    usuario = relationship("User", backref="paciente", uselist=False)
