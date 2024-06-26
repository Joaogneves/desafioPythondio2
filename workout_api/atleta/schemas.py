from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.contrib.schemas import BaseSchemas, OutMixin
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta


class Atleta(BaseSchemas):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900',min_length=11, max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example=28)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=80.0)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.75)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centros_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Ct do atleta')]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaOutDes(OutMixin):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    centros_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Ct do atleta')]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]

class AtletaUpdate(BaseSchemas):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=28)]
    peso: Annotated[Optional[PositiveFloat], Field(None, description='Peso do atleta', example=80.0)]
    altura: Annotated[Optional[PositiveFloat], Field(None, description='Altura do atleta', example=1.75)]