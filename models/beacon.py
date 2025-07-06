# models/beacon.py
"""
Modelo Beacon: representa um beacon de localização indoor.
Compatível com Pydantic (validação) e SQLAlchemy (ORM).
"""
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, String, Float
from models.base import Base

class BeaconORM(Base):
    __tablename__ = "beacons"
    mac = Column(String, primary_key=True) 
    posX = Column(Float, nullable=False)
    posY = Column(Float, nullable=False)
    label = Column(String, nullable=True)

class Beacon(BaseModel):
    mac: str
    posX: float
    posY: float
    label: Optional[str] = None

    class Config:
        from_attributes = True
