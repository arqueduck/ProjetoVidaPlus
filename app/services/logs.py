from typing import Optional

from sqlalchemy.orm import Session

from app.models.log import LogSistema
from app.models.user import User


def registrar_log(
    db: Session,
    acao: str,
    usuario: Optional[User] = None,
    detalhes: Optional[str] = None,
) -> None:
    """
    Registra um log simples no banco, associado ou não a um usuário.
    """
    log = LogSistema(
        usuario_id=usuario.id if usuario else None,
        acao=acao,
        detalhes=detalhes,
    )
    db.add(log)
    db.commit()
