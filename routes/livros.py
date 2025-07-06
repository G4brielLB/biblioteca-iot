# routes/livros.py
"""
Rotas para operações CRUD de Livro.

Como acessar os endpoints:

- Listar todos os livros:
  GET /livros/

- Obter um livro específico:
  GET /livros/{idLivro}

- Criar um novo livro:
  POST /livros/
  Body (JSON):
    {
      "idLivro": "string",
      "titulo": "string",
      "editora": "string",
      "codigoCutter": "string",
      "estanteId": "string"
    }

- Atualizar um livro:
  PUT /livros/{idLivro}
  Body (JSON): igual ao POST

- Remover um livro:
  DELETE /livros/{idLivro}

- Buscar livros pelo nome (título):
  GET /livros/buscar?q={termoBusca}

Todos os endpoints retornam/recebem JSON.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.livro import Livro, LivroORM
from models.instancia_livro import InstanciaLivro, InstanciaLivroORM
from db.session import get_db
import unicodedata

def remover_acentos(texto: str) -> str:
    """Remove acentos e normaliza texto para busca insensível a acentos."""
    return unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8').lower()

router = APIRouter(prefix="/livros", tags=["Livros"])

@router.get("/", response_model=List[Livro])
def listar_livros(db: Session = Depends(get_db)):
    """Lista todos os livros."""
    return db.query(LivroORM).all()

@router.get("/buscar", response_model=List[Livro])
def buscar_livros_por_nome(q: str, db: Session = Depends(get_db)):
    """Busca livros pelo nome (título), parcial e insensível a acentos e case."""
    # Normaliza o termo de busca (remove acentos e converte para minúsculas)
    termo_normalizado = remover_acentos(q)
    
    # Busca todos os livros e filtra em Python para comparação sem acentos
    todos_livros = db.query(LivroORM).all()
    livros_encontrados = []
    
    for livro in todos_livros:
        titulo_normalizado = remover_acentos(livro.titulo)
        if termo_normalizado in titulo_normalizado:
            livros_encontrados.append(livro)
    
    return livros_encontrados

@router.get("/{idLivro}/instancias", response_model=List[InstanciaLivro])
def listar_instancias_livro(idLivro: str, db: Session = Depends(get_db)):
    """Lista todas as instâncias de um livro específico."""
    # Verifica se o livro existe
    livro = db.query(LivroORM).filter(LivroORM.idLivro == idLivro).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    # Retorna as instâncias do livro
    return db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idLivro == idLivro).all()

@router.get("/{idLivro}", response_model=Livro)
def obter_livro(idLivro: str, db: Session = Depends(get_db)):
    """Retorna um livro específico pelo idLivro."""
    livro = db.query(LivroORM).filter(LivroORM.idLivro == idLivro).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@router.post("/", response_model=Livro, status_code=status.HTTP_201_CREATED)
def criar_livro(livro: Livro, db: Session = Depends(get_db)):
    """Cria um novo livro."""
    if db.query(LivroORM).filter(LivroORM.idLivro == livro.idLivro).first():
        raise HTTPException(status_code=400, detail="idLivro já cadastrado")
    novo = LivroORM(**livro.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{idLivro}", response_model=Livro)
def atualizar_livro(idLivro: str, livro: Livro, db: Session = Depends(get_db)):
    """Atualiza um livro existente."""
    obj = db.query(LivroORM).filter(LivroORM.idLivro == idLivro).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    for key, value in livro.dict().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{idLivro}", status_code=status.HTTP_204_NO_CONTENT)
def remover_livro(idLivro: str, db: Session = Depends(get_db)):
    """Remove um livro pelo idLivro."""
    obj = db.query(LivroORM).filter(LivroORM.idLivro == idLivro).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(obj)
    db.commit()
