from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.centro_treinamento.schemas import CentroTreinamentoOut, CentroTreinamentoIn
from workout_api.centro_treinamento.models import CentroTreinamentoModel


router = APIRouter();

@router.post(path='/', 
             summary='Criar novo centro de treinamento', 
             status_code=status.HTTP_201_CREATED, 
             response_model=CentroTreinamentoIn)
async def post(
    db_session: DatabaseDependency, centro_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    centro_out = CentroTreinamentoOut(id=uuid4(), **centro_in.model_dump())
    centro_model = CentroTreinamentoModel(**centro_out.model_dump())
    try:
        db_session.add(centro_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um CT com o nome: {centro_model.nome}")
    return centro_out

@router.get(path='/',
            summary='Consultar todos os centros de treinamento',
            status_code=status.HTTP_200_OK, 
            response_model=list[CentroTreinamentoOut])
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros: list[CentroTreinamentoOut] = (
        await db_session.execute(select(CentroTreinamentoModel))
    ).scalars().all()
    return centros


@router.get(path='/{id}', 
            summary='Consultar ct pelo id', 
            status_code=status.HTTP_200_OK, 
            response_model=CentroTreinamentoOut)
async def get(id:UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro: CentroTreinamentoOut = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()
    
    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Centro de treinamento com id '{id}' não foi encontrado.")

    return centro