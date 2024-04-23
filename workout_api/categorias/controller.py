from fastapi import APIRouter, status, Body, HTTPException
from pydantic import UUID4
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from workout_api.contrib.dependencies import DatabaseDependency
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel

router = APIRouter();

@router.post(path='/',
             summary='Criar nova categoria', 
             status_code=status.HTTP_201_CREATED, 
             response_model=CategoriaOut)
async def post(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    try:
        db_session.add(categoria_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um categoria com o nome: {categoria_model.nome}")
    return categoria_out

@router.get(path='/', 
            summary='Consultar todas as categorias', 
            status_code=status.HTTP_200_OK, 
            response_model=list[CategoriaOut])
async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (
        await db_session.execute(select(CategoriaModel))
    ).scalars().all()
    return categorias


@router.get(path='/{id}', 
            summary='Consultar categoria pelo id', 
            status_code=status.HTTP_200_OK, 
            response_model=CategoriaOut)
async def get(id:UUID4, db_session: DatabaseDependency) -> CategoriaOut:
    categoria: CategoriaOut = (
        await db_session.execute(select(CategoriaModel).filter_by(id=id))
    ).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com id '{id}' não foi encontrada.")

    return categoria