from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class LogSistema(Base):
    __tablename__ = "logs_sistema"

    id = Column(Integer, primary_key=True, index=True)

    # Pode ser nulo para ações sem usuário autenticado (ex.: falha de login)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    acao = Column(String, nullable=False)       # Ex.: "LOGIN_SUCESSO", "CRIAR_CONSULTA"
    detalhes = Column(Text, nullable=True)      # JSON/Texto livre com contexto
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("User", backref="logs")
