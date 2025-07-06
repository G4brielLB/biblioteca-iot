# routes/estantes.py
"""
Rotas para operações CRUD de Estante.

Como acessar os endpoints:

- Listar todas as estantes:
  GET /estantes/

- Obter uma estante específica:
  GET /estantes/{idEstante}

- Criar uma nova estante:
  POST /estantes/
  Body (JSON):
    {
      "idEstante": "string",
      "posX": float,
      "posY": float,
      "cor": "string",
      "codigosCutter": ["string", ...]
    }

- Atualizar uma estante:
  PUT /estantes/{idEstante}
  Body (JSON): igual ao POST

- Remover uma estante:
  DELETE /estantes/{idEstante}

Todos os endpoints retornam/recebem JSON.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.estante import Estante, EstanteORM
from db.session import get_db

router = APIRouter(prefix="/estantes", tags=["Estantes"])

@router.get("/", response_model=List[Estante])
def listar_estantes(db: Session = Depends(get_db)):
    """Lista todas as estantes."""
    return db.query(EstanteORM).all()

@router.get("/{idEstante}", response_model=Estante)
def obter_estante(idEstante: str, db: Session = Depends(get_db)):
    """Retorna uma estante específica pelo idEstante."""
    estante = db.query(EstanteORM).filter(EstanteORM.idEstante == idEstante).first()
    if not estante:
        raise HTTPException(status_code=404, detail="Estante não encontrada")
    return estante

@router.post("/", response_model=Estante, status_code=status.HTTP_201_CREATED)
def criar_estante(estante: Estante, db: Session = Depends(get_db)):
    """Cria uma nova estante."""
    if db.query(EstanteORM).filter(EstanteORM.idEstante == estante.idEstante).first():
        raise HTTPException(status_code=400, detail="idEstante já cadastrado")
    novo = EstanteORM(**estante.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{idEstante}", response_model=Estante)
def atualizar_estante(idEstante: str, estante: Estante, db: Session = Depends(get_db)):
    """Atualiza uma estante existente."""
    obj = db.query(EstanteORM).filter(EstanteORM.idEstante == idEstante).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Estante não encontrada")
    for key, value in estante.dict().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{idEstante}", status_code=status.HTTP_204_NO_CONTENT)
def remover_estante(idEstante: str, db: Session = Depends(get_db)):
    """Remove uma estante pelo idEstante."""
    obj = db.query(EstanteORM).filter(EstanteORM.idEstante == idEstante).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Estante não encontrada")
    db.delete(obj)
    db.commit()
