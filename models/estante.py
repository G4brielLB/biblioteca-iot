# models/estante.py
"""
Modelo Estante: representa uma estante da biblioteca.
Compatível com Pydantic (validação) e SQLAlchemy (ORM).
"""
from typing import List
from pydantic import BaseModel
from sqlalchemy import Column, String, Float
from models.base import Base
from sqlalchemy.types import JSON

class EstanteORM(Base):
    __tablename__ = "estantes"
    idEstante = Column(String, primary_key=True)
    posX = Column(Float, nullable=False)
    posY = Column(Float, nullable=False)
    cor = Column(String, nullable=False)
    codigosCutter = Column(JSON, nullable=False)  # Lista de strings

class Estante(BaseModel):
    idEstante: str
    posX: float
    posY: float
    cor: str
    codigosCutter: List[str]

    class Config:
        from_attributes = True
