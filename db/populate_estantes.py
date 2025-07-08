# db/populate_estantes.py
"""
Script para popular o banco de dados com 12 estantes conforme layout específico.
Execute este script após rodar o servidor FastAPI.
"""
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.estante import EstanteORM

# Estantes com posições, cores e códigos Cutter específicos
estantes_exemplo = [
    {"idEstante": "E1", "posX": 1.55, "posY": 0, "cor": "azul", "codigosCutter": ["C1"]},
    {"idEstante": "E2", "posX": 5.75, "posY": 0, "cor": "azul", "codigosCutter": ["C2"]},
    {"idEstante": "E3", "posX": 1.55, "posY": 0.7, "cor": "verde", "codigosCutter": ["C3"]},
    {"idEstante": "E4", "posX": 5.75, "posY": 0.7, "cor": "verde", "codigosCutter": ["C4"]},
    {"idEstante": "E5", "posX": 1.55, "posY": 1.55, "cor": "vermelho", "codigosCutter": ["C5"]},
    {"idEstante": "E6", "posX": 5.75, "posY": 1.55, "cor": "vermelho", "codigosCutter": ["C6"]},
    {"idEstante": "E7", "posX": 1.55, "posY": 2.25, "cor": "amarelo", "codigosCutter": ["C7"]},
    {"idEstante": "E8", "posX": 5.75, "posY": 2.25, "cor": "amarelo", "codigosCutter": ["C8"]},
    {"idEstante": "E9", "posX": 1.55, "posY": 3.1, "cor": "azul", "codigosCutter": ["C9"]},
    {"idEstante": "E10", "posX": 5.75, "posY": 3.1, "cor": "azul", "codigosCutter": ["C10"]},
    {"idEstante": "E11", "posX": 1.55, "posY": 3.8, "cor": "verde", "codigosCutter": ["C11"]},
    {"idEstante": "E12", "posX": 5.75, "posY": 3.8, "cor": "verde", "codigosCutter": ["C12"]},
]

def popular_estantes():
    db: Session = SessionLocal()
    
    # Apagar todas as estantes existentes
    db.query(EstanteORM).delete()
    
    # Inserir as novas estantes
    for estante in estantes_exemplo:
        db.add(EstanteORM(**estante))
    
    db.commit()
    db.close()

if __name__ == "__main__":
    popular_estantes()
    print("Estantes atualizadas com sucesso!")
    print("12 estantes inseridas com novas posições e cores.")
