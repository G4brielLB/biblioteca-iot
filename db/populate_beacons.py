# db/populate_beacons.py
"""
Script para popular o banco de dados com beacons de exemplo.
Execute este script após rodar o servidor FastAPI.
"""
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.beacon import BeaconORM

beacons_exemplo = [
    {"mac": "E0:5A:1B:77:25:3E", "posX": 1.0, "posY": 0.2, "label": "Beacon 1"},
    {"mac": "48:E7:29:97:3B:2E", "posX": 5.0, "posY": 1.6, "label": "Beacon 2"},
    {"mac": "48:E7:29:99:97:BE", "posX": 1.0, "posY": 3.4, "label": "Beacon 3"},
]

def popular_beacons():
    db: Session = SessionLocal()
    
    # Remover todos os beacons existentes
    db.query(BeaconORM).delete()
    print("Beacons existentes removidos.")
    
    # Adicionar os novos beacons
    for beacon in beacons_exemplo:
        db.add(BeaconORM(**beacon))
    
    db.commit()
    db.close()

if __name__ == "__main__":
    popular_beacons()
    print("Beacons atualizados com sucesso!")
