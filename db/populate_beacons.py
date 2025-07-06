# db/populate_beacons.py
"""
Script para popular o banco de dados com beacons de exemplo.
Execute este script após rodar o servidor FastAPI.
"""
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.beacon import BeaconORM

beacons_exemplo = [
    {"mac": "AA:BB:CC:DD:EE:01", "posX": 0.0, "posY": 0.0, "label": "Ponto A"},
    {"mac": "AA:BB:CC:DD:EE:02", "posX": 10.0, "posY": 0.0, "label": "Ponto B"},
    {"mac": "AA:BB:CC:DD:EE:03", "posX": 5.0, "posY": 8.66, "label": "Ponto C"},  # Triângulo equilátero
]

def popular_beacons():
    db: Session = SessionLocal()
    for beacon in beacons_exemplo:
        if not db.query(BeaconORM).filter(BeaconORM.mac == beacon["mac"]).first():
            db.add(BeaconORM(**beacon))
    db.commit()
    db.close()

if __name__ == "__main__":
    popular_beacons()
    print("Beacons de exemplo inseridos com sucesso!")
