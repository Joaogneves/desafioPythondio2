from fastapi import APIRouter
from workout_api.atleta.controller import router as atleta
from workout_api.categorias.controller import router as categoria
from workout_api.centro_treinamento.controller import router as centro

api_router = APIRouter();

api_router.include_router(atleta, prefix='/atletas', tags=['atletas'])
api_router.include_router(categoria, prefix='/categoria', tags=['categoria'])
api_router.include_router(centro, prefix='/centros_treinamento', tags=['centros_treinamento'])