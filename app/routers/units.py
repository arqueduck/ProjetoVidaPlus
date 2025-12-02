from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.unit import Unidade
from app.schemas.unit import UnidadeCreate, UnidadeRead, UnidadeUpdate

router = APIRouter(prefix="/unidades", tags=["Unidades"])


@router.post("/", response_model=UnidadeRead, status_code=status.HTTP_201_CREATED)
def criar_unidade(unidade_in: UnidadeCreate, db: Session = Depends(get_db)):
    unidade = Unidade(
        nome=unidade_in.nome,
        tipo_unidade=unidade_in.tipo_unidade,
        endereco=unidade_in.endereco,
        telefone=unidade_in.telefone,
    )
    db.add(unidade)
    db.commit()
    db.refresh(unidade)
    return unidade


@router.get("/", response_model=list[UnidadeRead])
def listar_unidades(db: Session = Depends(get_db)):
    return db.query(Unidade).all()


@router.get("/{unidade_id}", response_model=UnidadeRead)
def obter_unidade(unidade_id: int, db: Session = Depends(get_db)):
    unidade = db.get(Unidade, unidade_id)
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada.",
        )
    return unidade


@router.put("/{unidade_id}", response_model=UnidadeRead)
def atualizar_unidade(
    unidade_id: int,
    unidade_up: UnidadeUpdate,
    db: Session = Depends(get_db),
):
    unidade = db.get(Unidade, unidade_id)
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada.",
        )

    if unidade_up.nome is not None:
        unidade.nome = unidade_up.nome
    if unidade_up.tipo_unidade is not None:
        unidade.tipo_unidade = unidade_up.tipo_unidade
    if unidade_up.endereco is not None:
        unidade.endereco = unidade_up.endereco
    if unidade_up.telefone is not None:
        unidade.telefone = unidade_up.telefone

    db.commit()
    db.refresh(unidade)
    return unidade


@router.delete("/{unidade_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_unidade(unidade_id: int, db: Session = Depends(get_db)):
    unidade = db.get(Unidade, unidade_id)
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada.",
        )

    db.delete(unidade)
    db.commit()
    return
