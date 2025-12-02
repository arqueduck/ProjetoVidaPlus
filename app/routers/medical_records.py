from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db, get_current_user
from app.models.patient import Paciente
from app.models.professional import Profissional
from app.models.consultation import Consulta
from app.models.medical_record import Prontuario
from app.models.user import User
from app.schemas.medical_record import ProntuarioCreate, ProntuarioRead
from app.services.logs import registrar_log

router = APIRouter(prefix="/prontuarios", tags=["Prontuários"])


@router.post("/", response_model=ProntuarioRead, status_code=status.HTTP_201_CREATED)
def criar_prontuario(
    prontuario_in: ProntuarioCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # valida paciente
    paciente = db.get(Paciente, prontuario_in.paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paciente não encontrado.",
        )

    # valida profissional
    profissional = db.get(Profissional, prontuario_in.profissional_id)
    if not profissional:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profissional não encontrado.",
        )

    # se tiver consulta_id, valida consulta
    consulta = None
    if prontuario_in.consulta_id is not None:
        consulta = db.get(Consulta, prontuario_in.consulta_id)
        if not consulta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consulta não encontrada.",
            )

    db_prontuario = Prontuario(
        paciente_id=prontuario_in.paciente_id,
        profissional_id=prontuario_in.profissional_id,
        consulta_id=prontuario_in.consulta_id,
        descricao=prontuario_in.descricao,
        tipo_registro=prontuario_in.tipo_registro,
    )
    db.add(db_prontuario)
    db.commit()
    db.refresh(db_prontuario)
    
    registrar_log(
        db=db,
        acao="CRIAR_PRONTUARIO",
        usuario=current_user,
        detalhes=f"Prontuário ID={db_prontuario.id} criado pelo usuário ID={current_user.id}",
    )
    
    return db_prontuario


@router.get("/paciente/{paciente_id}", response_model=list[ProntuarioRead])
def listar_prontuarios_por_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # opcional: garantir que o paciente exista
    paciente = db.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado.",
        )

    registrar_log(
        db=db,
        acao="CRIAR_PRONTUARIO",
        usuario=current_user,
        detalhes=f"Prontuário ID={listar_prontuarios_por_paciente.id} criado pelo usuário ID={current_user.id}",
    )
    
    return (
        db.query(Prontuario)
        .filter(Prontuario.paciente_id == paciente_id)
        .order_by(Prontuario.data_registro.desc())
        .all()
    )


@router.get("/{prontuario_id}", response_model=ProntuarioRead)
def obter_prontuario(
    prontuario_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prontuario = db.get(Prontuario, prontuario_id)
    if not prontuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuário não encontrado.",
        )
        
    registrar_log(
        db=db,
        acao="CRIAR_PRONTUARIO",
        usuario=current_user,
        detalhes=f"Prontuário ID={obter_prontuario.id} criado pelo usuário ID={current_user.id}",
    )
    
    return prontuario
