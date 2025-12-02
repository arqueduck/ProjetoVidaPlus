from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models.user import User  
from app.models.consultation import Consulta
from app.models.patient import Paciente
from app.models.professional import Profissional
from app.models.unit import Unidade
from app.schemas.consultation import (
    ConsultaCreate,
    ConsultaRead,
    ConsultaUpdate,
    ConsultaStatusUpdate,
)
from app.services.logs import registrar_log

router = APIRouter(prefix="/consultas", tags=["Consultas"])


@router.post("/", response_model=ConsultaRead, status_code=status.HTTP_201_CREATED)
def criar_consulta(
    consulta_in: ConsultaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # valida se paciente existe
    if not db.get(Paciente, consulta_in.paciente_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paciente não encontrado.",
        )

    # valida se profissional existe
    if not db.get(Profissional, consulta_in.profissional_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profissional não encontrado.",
        )

    # valida se unidade existe
    if not db.get(Unidade, consulta_in.unidade_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unidade não encontrada.",
        )

    db_consulta = Consulta(
        paciente_id=consulta_in.paciente_id,
        profissional_id=consulta_in.profissional_id,
        unidade_id=consulta_in.unidade_id,
        data_hora=consulta_in.data_hora,
        tipo_atendimento=consulta_in.tipo_atendimento,
        status="AGENDADA",
        observacoes=consulta_in.observacoes,
    )
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    
    registrar_log(
        db=db,
        acao="CRIAR_CONSULTA",
        usuario=current_user,
        detalhes=f"Consulta ID={db_consulta.id} criada pelo usuário ID={current_user.id}",
    )
    
    return db_consulta


@router.get("/", response_model=list[ConsultaRead])
def listar_consultas(db: Session = Depends(get_db)):
    return db.query(Consulta).all()


@router.get("/{consulta_id}", response_model=ConsultaRead)
def obter_consulta(
    consulta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    consulta = db.query(Consulta).get(consulta_id)
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada.",
        )
        
    registrar_log(
        db=db,
        acao="CRIAR_CONSULTA",
        usuario=current_user,
        detalhes=f"Consulta ID={obter_consulta.id} criada pelo usuário ID={current_user.id}",
    )
    
    return consulta


@router.get("/pacientes/{paciente_id}", response_model=list[ConsultaRead])
def listar_consultas_por_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    registrar_log(
        db=db,
        acao="CRIAR_CONSULTA",
        usuario=current_user,
        detalhes=f"Consulta ID={listar_consultas_por_paciente.id} criada pelo usuário ID={current_user.id}",
    )
    
    return db.query(Consulta).filter(Consulta.paciente_id == paciente_id).all()


@router.get("/profissionais/{profissional_id}", response_model=list[ConsultaRead])
def listar_consultas_por_profissional(
    profissional_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    registrar_log(
        db=db,
        acao="CRIAR_CONSULTA",
        usuario=current_user,
        detalhes=f"Consulta ID={listar_consultas_por_profissional.id} criada pelo usuário ID={current_user.id}",
    )
    
    return (
        db.query(Consulta)
        .filter(Consulta.profissional_id == profissional_id)
        .all()
    )
    


@router.put("/{consulta_id}", response_model=ConsultaRead)
def atualizar_consulta(
    consulta_id: int,
    consulta_up: ConsultaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    consulta = db.query(Consulta).get(consulta_id)
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada.",
        )

    # se atualizar IDs, valida existência
    if consulta_up.paciente_id is not None:
        if not db.query(Paciente).get(consulta_up.paciente_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Paciente não encontrado.",
            )
        consulta.paciente_id = consulta_up.paciente_id

    if consulta_up.profissional_id is not None:
        if not db.query(Profissional).get(consulta_up.profissional_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Profissional não encontrado.",
            )
        consulta.profissional_id = consulta_up.profissional_id

    if consulta_up.unidade_id is not None:
        if not db.query(Unidade).get(consulta_up.unidade_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unidade não encontrada.",
            )
        consulta.unidade_id = consulta_up.unidade_id

    if consulta_up.data_hora is not None:
        consulta.data_hora = consulta_up.data_hora
    if consulta_up.tipo_atendimento is not None:
        consulta.tipo_atendimento = consulta_up.tipo_atendimento
    if consulta_up.observacoes is not None:
        consulta.observacoes = consulta_up.observacoes

    db.commit()
    db.refresh(consulta)
    
    registrar_log(
        db=db,
        acao="CRIAR_CONSULTA",
        usuario=current_user,
        detalhes=f"Consulta ID={atualizar_consulta.id} criada pelo usuário ID={current_user.id}",
    )

    return consulta


@router.patch("/{consulta_id}/status", response_model=ConsultaRead)
def atualizar_status_consulta(
    consulta_id: int,
    status_in: ConsultaStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    consulta = db.query(Consulta).get(consulta_id)
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada.",
        )

    consulta.status = status_in.status
    db.commit()
    db.refresh(consulta)
    
    registrar_log(
        db=db,
        acao="CRIAR_CONSULTA",
        usuario=current_user,
        detalhes=(
            f"Status da consulta ID={consulta.id} atualizado para "
            f"{consulta.status} pelo usuário ID={current_user.id}",
        )
    )
    
    return consulta
