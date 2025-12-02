from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.deps import get_db
from app.models.user import User
from app.models.professional import Profissional
from app.schemas.professional import (
    ProfissionalCreate,
    ProfissionalRead,
    ProfissionalUpdate,
)

router = APIRouter(prefix="/profissionais", tags=["Profissionais"])


@router.post("/", response_model=ProfissionalRead, status_code=status.HTTP_201_CREATED)
def criar_profissional(
    profissional_in: ProfissionalCreate,
    db: Session = Depends(get_db),
):
    # 1) Verifica se email já existe
    existing_user = db.query(User).filter(User.email == profissional_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado.",
        )

    # 2) Verifica se CPF já existe
    existing_cpf = db.query(Profissional).filter(
        Profissional.cpf == profissional_in.cpf
    ).first()
    if existing_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado.",
        )

    # 3) Cria o usuário vinculado (tipo PROFISSIONAL)
    hashed_password = get_password_hash(profissional_in.senha)

    db_user = User(
        nome_completo=profissional_in.nome_completo,
        email=profissional_in.email,
        senha_hash=hashed_password,
        tipo="PROFISSIONAL",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 4) Cria o profissional
    db_prof = Profissional(
        usuario_id=db_user.id,
        cpf=profissional_in.cpf,
        registro_conselho=profissional_in.registro_conselho,
        tipo_conselho=profissional_in.tipo_conselho,
        especialidade=profissional_in.especialidade,
        unidade_id=profissional_in.unidade_id,
    )
    db.add(db_prof)
    db.commit()
    db.refresh(db_prof)

    return ProfissionalRead(
        id=db_prof.id,
        usuario_id=db_user.id,
        nome_completo=db_user.nome_completo,
        email=db_user.email,
        cpf=db_prof.cpf,
        registro_conselho=db_prof.registro_conselho,
        tipo_conselho=db_prof.tipo_conselho,
        especialidade=db_prof.especialidade,
        unidade_id=db_prof.unidade_id,
    )


@router.get("/", response_model=list[ProfissionalRead])
def listar_profissionais(db: Session = Depends(get_db)):
    profissionais = db.query(Profissional).all()
    result: list[ProfissionalRead] = []
    for p in profissionais:
        u = p.usuario
        result.append(
            ProfissionalRead(
                id=p.id,
                usuario_id=u.id,
                nome_completo=u.nome_completo,
                email=u.email,
                cpf=p.cpf,
                registro_conselho=p.registro_conselho,
                tipo_conselho=p.tipo_conselho,
                especialidade=p.especialidade,
                unidade_id=p.unidade_id,
            )
        )
    return result


@router.get("/{profissional_id}", response_model=ProfissionalRead)
def obter_profissional(
    profissional_id: int,
    db: Session = Depends(get_db),
):
    p = db.get(Profissional, profissional_id)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado.",
        )
    u = p.usuario
    return ProfissionalRead(
        id=p.id,
        usuario_id=u.id,
        nome_completo=u.nome_completo,
        email=u.email,
        cpf=p.cpf,
        registro_conselho=p.registro_conselho,
        tipo_conselho=p.tipo_conselho,
        especialidade=p.especialidade,
        unidade_id=p.unidade_id,
    )


@router.put("/{profissional_id}", response_model=ProfissionalRead)
def atualizar_profissional(
    profissional_id: int,
    profissional_up: ProfissionalUpdate,
    db: Session = Depends(get_db),
):
    p = db.get(Profissional, profissional_id)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado.",
        )

    if profissional_up.registro_conselho is not None:
        p.registro_conselho = profissional_up.registro_conselho
    if profissional_up.tipo_conselho is not None:
        p.tipo_conselho = profissional_up.tipo_conselho
    if profissional_up.especialidade is not None:
        p.especialidade = profissional_up.especialidade
    if profissional_up.unidade_id is not None:
        p.unidade_id = profissional_up.unidade_id

    db.commit()
    db.refresh(p)

    u = p.usuario
    return ProfissionalRead(
        id=p.id,
        usuario_id=u.id,
        nome_completo=u.nome_completo,
        email=u.email,
        cpf=p.cpf,
        registro_conselho=p.registro_conselho,
        tipo_conselho=p.tipo_conselho,
        especialidade=p.especialidade,
        unidade_id=p.unidade_id,
    )


@router.delete("/{profissional_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_profissional(
    profissional_id: int,
    db: Session = Depends(get_db),
):
    p = db.get(Profissional, profissional_id)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profissional não encontrado.",
        )

    db.delete(p)
    db.commit()
    return
