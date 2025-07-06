# db/populate_livros.py
"""
Script para popular o banco de dados com livros de exemplo.
Os códigos Cutter dos livros são compatíveis com os das estantes.
Execute este script após rodar o servidor FastAPI e popular as estantes.
"""
from sqlalchemy.orm import Session
from db.session import SessionLocal
from models.livro import LivroORM

livros_exemplo = [
    {"idLivro": "978-85-01-00001-1", "titulo": "Cálculo I", "editora": "Editora Alfa", "codigoCutter": "C01", "estanteId": "E1"},
    {"idLivro": "978-85-01-00002-2", "titulo": "Cálculo II", "editora": "Editora Beta", "codigoCutter": "C02", "estanteId": "E2"},
    {"idLivro": "978-85-01-00003-3", "titulo": "Álgebra Linear", "editora": "Editora Gama", "codigoCutter": "C03", "estanteId": "E3"},
    {"idLivro": "978-85-01-00004-4", "titulo": "Geometria Analítica", "editora": "Editora Delta", "codigoCutter": "C04", "estanteId": "E4"},
    {"idLivro": "978-85-01-00005-5", "titulo": "Física I", "editora": "Editora Epsilon", "codigoCutter": "C05", "estanteId": "E5"},
    {"idLivro": "978-85-01-00006-6", "titulo": "Física II", "editora": "Editora Zeta", "codigoCutter": "C06", "estanteId": "E6"},
    {"idLivro": "978-85-01-00007-7", "titulo": "Química Geral", "editora": "Editora Eta", "codigoCutter": "C07", "estanteId": "E7"},
    {"idLivro": "978-85-01-00008-8", "titulo": "Química Orgânica", "editora": "Editora Teta", "codigoCutter": "C08", "estanteId": "E8"},
    {"idLivro": "978-85-01-00009-9", "titulo": "Programação Python", "editora": "Editora Theta", "codigoCutter": "C09", "estanteId": "E9"},
    {"idLivro": "978-85-01-00010-0", "titulo": "Estruturas de Dados", "editora": "Editora Iota", "codigoCutter": "C10", "estanteId": "E10"},
    {"idLivro": "978-85-01-00011-1", "titulo": "Banco de Dados", "editora": "Editora Kappa", "codigoCutter": "C11", "estanteId": "E11"},
    {"idLivro": "978-85-01-00012-2", "titulo": "Redes de Computadores", "editora": "Editora Lambda", "codigoCutter": "C12", "estanteId": "E12"},
]

def popular_livros():
    db: Session = SessionLocal()
    for livro in livros_exemplo:
        if not db.query(LivroORM).filter(LivroORM.idLivro == livro["idLivro"]).first():
            db.add(LivroORM(**livro))
    db.commit()
    db.close()

if __name__ == "__main__":
    popular_livros()
    print("Livros de exemplo inseridos com sucesso!")
