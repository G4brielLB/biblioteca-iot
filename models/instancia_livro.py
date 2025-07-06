# models/instancia_livro.py
"""
Modelo InstanciaLivro: representa um exemplar físico de um livro.
Compatível com Pydantic (validação) e SQLAlchemy (ORM).
"""
from datetime import datetime
from typing import Literal
from pydantic import BaseModel
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from models.base import Base

class InstanciaLivroORM(Base):
    __tablename__ = "instancias_livro"
    idInstancia = Column(String, primary_key=True)  # QR/barcode
    idLivro = Column(String, ForeignKey("livros.idLivro"), nullable=False)  # FK para Livro
    posX = Column(Float, nullable=False)
    prateleira = Column(String, nullable=False)  # Ex: "CIMA", "MEIO", "BAIXO"
    situacao = Column(String, nullable=False)  # Ex: "disponivel", "emprestado", "cativo"
    ultimaAtualizacao = Column(DateTime, nullable=False)

class InstanciaLivro(BaseModel):
    idInstancia: str
    idLivro: str
    posX: float
    prateleira: Literal["CIMA", "MEIO", "BAIXO"]
    situacao: Literal["disponivel", "emprestado", "cativo"]
    ultimaAtualizacao: datetime

    class Config:
        from_attributes = True
