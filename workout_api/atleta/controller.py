from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Body
from uuid import uuid4
from fastapi_pagination import paginate, LimitOffsetPage
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoOut
from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate, AtletaOutDes
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaOut

router = APIRouter()

@router.post(path='/', 
             summary='Criar novo atleta', 
             status_code=status.HTTP_201_CREATED, 
             response_model=AtletaOut)
async def post(
    db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)
) -> AtletaOut:
    categoria: CategoriaOut = (
        await db_session.execute(
            select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome))
        ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Categoria '{atleta_in.categoria.nome}' não foi encontrada.")

    centro_terinamento: CentroTreinamentoOut = (
        await db_session.execute(
            select(CentroTreinamentoModel).filter_by(nome=atleta_in.centros_treinamento.nome))
        ).scalars().first()

    if not centro_terinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ct '{atleta_in.centros_treinamento.nome}' não foi encontrado.")

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now() , **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centros_treinamento'}))
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centros_treinamento_id = centro_terinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o cpf: {atleta_model.cpf}")

    return atleta_model


@router.get(path='/', 
            summary='Consultar todos os atletas', 
            status_code=status.HTTP_200_OK, 
            response_model=LimitOffsetPage[AtletaOutDes])
async def query(db_session: DatabaseDependency, nome:str = '', cpf:str = '') -> LimitOffsetPage[AtletaOutDes]:
    atletas_res = []
    if nome:
        atletas: LimitOffsetPage[AtletaOutDes] = (
            await db_session.execute(select(AtletaModel).filter_by(nome=nome))
        ).scalars().all()
    elif cpf:
        atletas: LimitOffsetPage[AtletaOutDes] = (
            await db_session.execute(select(AtletaModel).filter_by(cpf=cpf))
        ).scalars().all()
    else:
        atletas: LimitOffsetPage[AtletaOutDes] = (
            await db_session.execute(select(AtletaModel))
        ).scalars().all()

    atletas_res = [
        AtletaOutDes.model_validate(atleta) 
        for atleta in atletas
        ]
    
    return paginate(atletas_res)

@router.get(path='/{id}', 
            summary='Consultar atleta pelo id', 
            status_code=status.HTTP_200_OK, 
            response_model=AtletaOut)
async def get(id:UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com id '{id}' não foi encontrado.")

    return atleta


@router.patch(path='/{id}', 
            summary='Editar atleta pelo id', 
            status_code=status.HTTP_200_OK, 
            response_model=AtletaOut)
async def patch(id:UUID4, 
                db_session: DatabaseDependency,
                atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com id '{id}' não foi encontrado.")

    atleta_update = atleta_up.model_dump(exclude_unset=True)

    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)
    return atleta

@router.delete(path='/{id}', 
            summary='Deletar atleta pelo id', 
            status_code=status.HTTP_204_NO_CONTENT)
async def delete(id:UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()
    
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Atleta com id '{id}' não foi encontrado.")

    await db_session.delete(atleta)
    await db_session.commit()
