# models/livro.py
"""
Modelo Livro: representa uma obra conceitual da biblioteca.
Compatível com Pydantic (validação) e SQLAlchemy (ORM).
"""
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String
from models.base import Base

class LivroORM(Base):
    __tablename__ = "livros"
    idLivro = Column(String, primary_key=True)  # ISBN
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)  # Novo campo autor
    editora = Column(String, nullable=False)
    codigoCutter = Column(String, nullable=False)
    estanteId = Column(String, nullable=False)  # FK para Estante

class Livro(BaseModel):
    idLivro: str
    titulo: str
    autor: str  # Novo campo autor
    editora: str
    codigoCutter: str
    estanteId: str

    class Config:
        from_attributes = True
