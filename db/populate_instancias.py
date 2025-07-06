# db/populate_instancias.py
"""
Script para popular o banco de dados com instâncias de livros de exemplo.
Cada livro terá várias instâncias, com diferentes situações.
Execute este script após rodar o servidor FastAPI e popular os livros.
"""
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.instancia_livro import InstanciaLivroORM
# Importa todos os modelos para garantir que as tabelas sejam reconhecidas
from models.beacon import BeaconORM
from models.estante import EstanteORM
from models.livro import LivroORM
from datetime import datetime, timedelta

instancias_exemplo = []
prateleiras = ["CIMA", "MEIO", "BAIXO"]
situacoes = ["disponivel", "emprestado", "cativo"]

for i in range(1, 13):  # Para cada livro
    idLivro = f"978-85-01-000{i:02d}-{i%10}"
    for j in range(1, 6):  # 5 instâncias por livro
        idInstancia = f"{idLivro}-EX{j}"
        posX = 1.75 if i <= 6 else 6.25  # Coluna 1 ou 2 (novas posições)
        prateleira = prateleiras[j % 3]
        # Situação: maioria disponível, alguns emprestados/cativos
        if j == 2:
            situacao = "emprestado"
        elif j == 4:
            situacao = "cativo"
        else:
            situacao = "disponivel"
        ultimaAtualizacao = datetime.now() - timedelta(days=j)
        instancias_exemplo.append({
            "idInstancia": idInstancia,
            "idLivro": idLivro,
            "posX": posX + 0.1 * j,  # Pequena variação
            "prateleira": prateleira,
            "situacao": situacao,
            "ultimaAtualizacao": ultimaAtualizacao
        })

def popular_instancias():
    db: Session = SessionLocal()
    for instancia in instancias_exemplo:
        if not db.query(InstanciaLivroORM).filter(InstanciaLivroORM.idInstancia == instancia["idInstancia"]).first():
            db.add(InstanciaLivroORM(**instancia))
    db.commit()
    db.close()

if __name__ == "__main__":
    popular_instancias()
    print("Instâncias de livros de exemplo inseridas com sucesso!")
