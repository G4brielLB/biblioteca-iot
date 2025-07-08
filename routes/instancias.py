# routes/instancias.py
"""
Rotas para operações CRUD de InstanciaLivro e endpoints de navegação.

Como acessar os endpoints:

- Listar todas as instâncias:
  GET /instancias/
  → Retorna todas as instâncias de livros cadastradas.

- Obter uma instância específica:
  GET /instancias/{idInstancia}
  → Retorna os dados de uma instância pelo seu idInstancia.

- Listar instâncias de um livro:
  GET /livros/{idLivro}/instancias
  → Retorna todas as instâncias físicas de um livro (exemplares).

- Criar uma nova instância:
  POST /instancias/
  Body (JSON):
    {
      "idInstancia": "string",
      "idLivro": "string",
      "posX": float,
      "situacao": "disponivel|emprestado|cativo",
      "ultimaAtualizacao": "YYYY-MM-DDTHH:MM:SS"
    }

- Atualizar uma instância:
  PUT /instancias/{idInstancia}
  Body (JSON): igual ao POST

- Remover uma instância:
  DELETE /instancias/{idInstancia}

- Buscar livros pelo nome/título (com instâncias):
  GET /instancias/livros/buscar?q=termo
  → Retorna uma lista de objetos:
    {
      "livro": {dados do livro},
      "instancias": [lista de instâncias desse livro]
    }
  Exemplo: /instancias/livros/buscar?q=calculo

- Detalhes completos de uma instância (inclui localização e beacons):
  GET /instancias/{idInstancia}/detalhes
  → Retorna um objeto:
    {
      "instancia": {dados da instância},
      "livro": {dados do livro},
      "estante": {dados da estante},
      "beacons": [lista de beacons]
    }
  Exemplo: /instancias/123456/detalhes

- Emprestar um livro (disponivel → emprestado):
  POST /instancias/{idInstancia}/emprestar
  → Altera situação para "emprestado" se estiver "disponivel"
  → Livros "cativo" não podem ser emprestados
  Exemplo: /instancias/123456/emprestar

- Devolver um livro (emprestado → disponivel):
  POST /instancias/{idInstancia}/devolver
  Body (JSON):
    {
      "nova_posX": float
    }
  → Altera situação para "disponivel" e atualiza posição
  → Apenas livros "emprestado" podem ser devolvidos
  Exemplo: /instancias/123456/devolver com body {"nova_posX": 1.8}

Todos os endpoints retornam/recebem JSON.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
from models.instancia_livro import InstanciaLivro, InstanciaLivroORM
from models.livro import LivroORM
from models.beacon import BeaconORM
from models.estante import EstanteORM
from db.session import get_db
from sqlalchemy.orm import joinedload
from schemas.instancia_schemas import LivroComInstancias, DetalhesInstancia, DevolucaoRequest
from datetime import datetime

router = APIRouter(prefix="/instancias", tags=["InstanciasLivro"])

@router.get("/", response_model=List[InstanciaLivro])
def listar_instancias(db: Session = Depends(get_db)):
    """Lista todas as instâncias de livro."""
    return db.query(InstanciaLivroORM).all()

@router.get("/{idInstancia}", response_model=InstanciaLivro)
def obter_instancia(idInstancia: str, db: Session = Depends(get_db)):
    """Retorna uma instância específica pelo idInstancia."""
    instancia = db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == idInstancia).first()
    if not instancia:
        raise HTTPException(status_code=404, detail="Instância não encontrada")
    return instancia

@router.get("/livros/{idLivro}/instancias", response_model=List[InstanciaLivro])
def listar_instancias_livro(idLivro: str, db: Session = Depends(get_db)):
    """Lista todas as instâncias de um livro."""
    return db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idLivro == idLivro).all()

@router.post("/", response_model=InstanciaLivro, status_code=status.HTTP_201_CREATED)
def criar_instancia(instancia: InstanciaLivro, db: Session = Depends(get_db)):
    """Cria uma nova instância de livro."""
    if db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == instancia.idInstancia).first():
        raise HTTPException(status_code=400, detail="idInstancia já cadastrado")
    novo = InstanciaLivroORM(**instancia.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{idInstancia}", response_model=InstanciaLivro)
def atualizar_instancia(idInstancia: str, instancia: InstanciaLivro, db: Session = Depends(get_db)):
    """Atualiza uma instância de livro existente."""
    obj = db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == idInstancia).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Instância não encontrada")
    for key, value in instancia.dict().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{idInstancia}", status_code=status.HTTP_204_NO_CONTENT)
def remover_instancia(idInstancia: str, db: Session = Depends(get_db)):
    """Remove uma instância pelo idInstancia."""
    obj = db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == idInstancia).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Instância não encontrada")
    db.delete(obj)
    db.commit()

"""
@router.get("/livros/buscar", response_model=List[LivroComInstancias])
def buscar_livros_com_instancias(q: str, db: Session = Depends(get_db)):
    #Busca livros pelo nome (título) e retorna cada livro com suas instâncias.
    livros = db.query(LivroORM).filter(LivroORM.titulo.ilike(f"%{q}%")).all()
    result = []
    for livro in livros:
        instancias = db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idLivro == livro.idLivro).all()
        result.append(LivroComInstancias(livro=livro, instancias=instancias))
    return result
"""
    
@router.get("/{idInstancia}/detalhes", response_model=DetalhesInstancia)
def detalhes_instancia(idInstancia: str, db: Session = Depends(get_db)):
    """Retorna detalhes da instância, incluindo posição e todos os beacons."""
    instancia = db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == idInstancia).first()
    if not instancia:
        raise HTTPException(status_code=404, detail="Instância não encontrada")
    livro = db.query(LivroORM).filter(LivroORM.idLivro == instancia.idLivro).first()
    estante = db.query(EstanteORM).filter(EstanteORM.idEstante == livro.estanteId).first() if livro else None
    beacons = db.query(BeaconORM).all()
    return DetalhesInstancia(
        instancia=instancia,
        livro=livro,
        estante=estante,
        beacons=beacons
    )

@router.post("/{idInstancia}/emprestar", response_model=InstanciaLivro)
def emprestar_livro(idInstancia: str, db: Session = Depends(get_db)):
    """Empresta um livro (disponivel → emprestado). Livros cativos não podem ser emprestados."""
    instancia = db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == idInstancia).first()
    if not instancia:
        raise HTTPException(status_code=404, detail="Instância não encontrada")
    
    if instancia.situacao == "emprestado":
        raise HTTPException(status_code=400, detail="Livro já está emprestado")
    
    if instancia.situacao == "cativo":
        raise HTTPException(status_code=400, detail="Livro cativo não pode ser emprestado")
    
    # Atualiza para emprestado
    instancia.situacao = "emprestado"
    instancia.ultimaAtualizacao = datetime.now()
    
    db.commit()
    db.refresh(instancia)
    return instancia

@router.post("/{idInstancia}/devolver", response_model=InstanciaLivro)
def devolver_livro(
    idInstancia: str, 
    devolucao_data: DevolucaoRequest,
    db: Session = Depends(get_db)
):
    """Devolve um livro (emprestado → disponivel) e atualiza sua posição na estante."""
    instancia = db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == idInstancia).first()
    if not instancia:
        raise HTTPException(status_code=404, detail="Instância não encontrada")
    
    if instancia.situacao != "emprestado":
        raise HTTPException(status_code=400, detail="Apenas livros emprestados podem ser devolvidos")
    
    # Atualiza situação e posição
    instancia.situacao = "disponivel"
    instancia.posX = devolucao_data.nova_posX
    instancia.ultimaAtualizacao = datetime.now()
    
    db.commit()
    db.refresh(instancia)
    return instancia
