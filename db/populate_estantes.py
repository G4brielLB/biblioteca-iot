# db/populate_estantes.py
"""
Script para popular o banco de dados com 12 estantes de exemplo (2 colunas com 6 cada, estantes coladas aos pares).
Execute este script após rodar o servidor FastAPI.
"""
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.estante import EstanteORM

estantes_exemplo = []
colunas_x = [1.75, 6.25]  # Duas colunas com 3.5m cada + 1m entre elas
for col in range(2):
    for row in range(6):
        id_estante = f"E{col*6+row+1}"
        pos_x = colunas_x[col]
        pos_y = 1.0 + row * 1.5  # Espaçamento vertical
        cor = "azul" if col == 0 else "verde"
        codigos_cutter = [f"C{col*6+row+1:02d}"]
        estantes_exemplo.append({
            "idEstante": id_estante,
            "posX": pos_x,
            "posY": pos_y,
            "cor": cor,
            "codigosCutter": codigos_cutter
        })

def popular_estantes():
    db: Session = SessionLocal()
    for estante in estantes_exemplo:
        if not db.query(EstanteORM).filter(EstanteORM.idEstante == estante["idEstante"]).first():
            db.add(EstanteORM(**estante))
    db.commit()
    db.close()

if __name__ == "__main__":
    popular_estantes()
    print("Estantes de exemplo inseridas com sucesso!")
