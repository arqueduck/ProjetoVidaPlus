from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Profissional(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), unique=True, nullable=False)

    cpf = Column(String, unique=True, nullable=False)
    registro_conselho = Column(String, nullable=False)  # ex.: número do CRM/COREN
    tipo_conselho = Column(String, nullable=False)      # ex.: "CRM", "COREN"
    especialidade = Column(String, nullable=False)      # ex.: "Cardiologia"
    # vamos deixar só como inteiro por enquanto; depois conectamos com a tabela de unidades
    unidade_id = Column(Integer, nullable=True)

    usuario = relationship("User", backref="profissional", uselist=False)
