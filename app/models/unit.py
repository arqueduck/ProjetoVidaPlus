from sqlalchemy import Column, Integer, String
from app.database import Base


class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    tipo_unidade = Column(String, nullable=False)   # HOSPITAL, CLINICA, LABORATORIO, HOMECARE
    endereco = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
