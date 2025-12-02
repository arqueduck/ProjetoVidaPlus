from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.patient import Paciente
from app.core.security import get_password_hash
from app.deps import get_db
from app.schemas.patient import (
    PacienteCreate,
    PacienteRead,
    PacienteUpdate,
)

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.post("/", response_model=PacienteRead, status_code=status.HTTP_201_CREATED)
def criar_paciente(paciente_in: PacienteCreate, db: Session = Depends(get_db)):
    # 1) Verifica se email já existe
    existing_user = (
        db.query(User)
        .filter(User.email == paciente_in.email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado.",
        )

    # 2) Verifica se CPF já existe
    existing_cpf = (
        db.query(Paciente)
        .filter(Paciente.cpf == paciente_in.cpf)
        .first()
    )
    if existing_cpf:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já cadastrado.",
        )

    # 3) Cria o usuário vinculado (tipo PACIENTE)
    hashed_password = get_password_hash(paciente_in.senha)

    db_user = User(
        nome_completo=paciente_in.nome_completo,
        email=paciente_in.email,
        senha_hash=hashed_password,
        tipo="PACIENTE",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 4) Cria o paciente
    db_paciente = Paciente(
        usuario_id=db_user.id,
        cpf=paciente_in.cpf,
        data_nascimento=paciente_in.data_nascimento,
        telefone=paciente_in.telefone,
        endereco=paciente_in.endereco,
        plano_saude=paciente_in.plano_saude,
        numero_carteirinha=paciente_in.numero_carteirinha,
    )
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)

    # Monta objeto de retorno combinando info de user + paciente
    return PacienteRead(
        id=db_paciente.id,
        usuario_id=db_user.id,
        nome_completo=db_user.nome_completo,
        email=db_user.email,
        cpf=db_paciente.cpf,
        data_nascimento=db_paciente.data_nascimento,
        telefone=db_paciente.telefone,
        endereco=db_paciente.endereco,
        plano_saude=db_paciente.plano_saude,
        numero_carteirinha=db_paciente.numero_carteirinha,
    )


@router.get("/", response_model=list[PacienteRead])
def listar_pacientes(db: Session = Depends(get_db)):
    pacientes = db.query(Paciente).all()
    result: list[PacienteRead] = []
    for p in pacientes:
        u = p.usuario
        result.append(
            PacienteRead(
                id=p.id,
                usuario_id=u.id,
                nome_completo=u.nome_completo,
                email=u.email,
                cpf=p.cpf,
                data_nascimento=p.data_nascimento,
                telefone=p.telefone,
                endereco=p.endereco,
                plano_saude=p.plano_saude,
                numero_carteirinha=p.numero_carteirinha,
            )
        )
    return result


@router.get("/{paciente_id}", response_model=PacienteRead)
def obter_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado.",
        )
    u = paciente.usuario
    return PacienteRead(
        id=paciente.id,
        usuario_id=u.id,
        nome_completo=u.nome_completo,
        email=u.email,
        cpf=paciente.cpf,
        data_nascimento=paciente.data_nascimento,
        telefone=paciente.telefone,
        endereco=paciente.endereco,
        plano_saude=paciente.plano_saude,
        numero_carteirinha=paciente.numero_carteirinha,
    )


@router.put("/{paciente_id}", response_model=PacienteRead)
def atualizar_paciente(
    paciente_id: int,
    paciente_up: PacienteUpdate,
    db: Session = Depends(get_db),
):
    paciente = db.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado.",
        )

    # Atualiza apenas os campos enviados
    if paciente_up.telefone is not None:
        paciente.telefone = paciente_up.telefone
    if paciente_up.endereco is not None:
        paciente.endereco = paciente_up.endereco
    if paciente_up.plano_saude is not None:
        paciente.plano_saude = paciente_up.plano_saude
    if paciente_up.numero_carteirinha is not None:
        paciente.numero_carteirinha = paciente_up.numero_carteirinha

    db.commit()
    db.refresh(paciente)

    u = paciente.usuario
    return PacienteRead(
        id=paciente.id,
        usuario_id=u.id,
        nome_completo=u.nome_completo,
        email=u.email,
        cpf=paciente.cpf,
        data_nascimento=paciente.data_nascimento,
        telefone=paciente.telefone,
        endereco=paciente.endereco,
        plano_saude=paciente.plano_saude,
        numero_carteirinha=paciente.numero_carteirinha,
    )


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.get(Paciente, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado.",
        )

    db.delete(paciente)
    db.commit()
    return
