from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchemas


class CentroTreinamentoIn(BaseSchemas):
    nome: Annotated[str, Field(description='Nome do ct', example='King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do ct', example='Rua x, 123', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietario do ct', example='Marcos', max_length=30)]

class CentroTreinamentoAtleta(BaseSchemas):
    nome: Annotated[str, Field(description='Nome do ct', example='King', max_length=20)]


class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do ct')]