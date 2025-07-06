# routes/beacons.py
"""
Rotas para operações CRUD de Beacon.

Como acessar os endpoints:

- Listar todos os beacons:
  GET /beacons/

- Obter um beacon específico:
  GET /beacons/{mac}

- Criar um novo beacon:
  POST /beacons/
  Body (JSON):
    {
      "mac": "string",
      "posX": float,
      "posY": float,
      "label": "string (opcional)"
    }

- Atualizar um beacon:
  PUT /beacons/{mac}
  Body (JSON): igual ao POST

- Remover um beacon:
  DELETE /beacons/{mac}

Todos os endpoints retornam/recebem JSON.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.beacon import Beacon, BeaconORM
from db.session import get_db

router = APIRouter(prefix="/beacons", tags=["Beacons"])

@router.get("/", response_model=List[Beacon])
def listar_beacons(db: Session = Depends(get_db)):
    """Lista todos os beacons."""
    return db.query(BeaconORM).all()

@router.get("/{mac}", response_model=Beacon)
def obter_beacon(mac: str, db: Session = Depends(get_db)):
    """Retorna um beacon específico pelo MAC."""
    beacon = db.query(BeaconORM).filter(BeaconORM.mac == mac).first()
    if not beacon:
        raise HTTPException(status_code=404, detail="Beacon não encontrado")
    return beacon

@router.post("/", response_model=Beacon, status_code=status.HTTP_201_CREATED)
def criar_beacon(beacon: Beacon, db: Session = Depends(get_db)):
    """Cria um novo beacon."""
    if db.query(BeaconORM).filter(BeaconORM.mac == beacon.mac).first():
        raise HTTPException(status_code=400, detail="MAC já cadastrado")
    novo = BeaconORM(**beacon.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.put("/{mac}", response_model=Beacon)
def atualizar_beacon(mac: str, beacon: Beacon, db: Session = Depends(get_db)):
    """Atualiza um beacon existente."""
    obj = db.query(BeaconORM).filter(BeaconORM.mac == mac).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Beacon não encontrado")
    for key, value in beacon.dict().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{mac}", status_code=status.HTTP_204_NO_CONTENT)
def remover_beacon(mac: str, db: Session = Depends(get_db)):
    """Remove um beacon pelo MAC."""
    obj = db.query(BeaconORM).filter(BeaconORM.mac == mac).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Beacon não encontrado")
    db.delete(obj)
    db.commit()
