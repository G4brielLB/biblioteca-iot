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
    # Estante E1 (códigos C01) - Matemática/Cálculo
    {"idLivro": "978-85-01-00001-1", "titulo": "Cálculo Volume 1", "autor": "James Stewart", "editora": "Cengage Learning", "codigoCutter": "C01", "estanteId": "E1"},
    {"idLivro": "978-85-01-00002-2", "titulo": "Cálculo Volume 2", "autor": "James Stewart", "editora": "Cengage Learning", "codigoCutter": "C01", "estanteId": "E1"},
    
    # Estante E2 (códigos C02) - Álgebra
    {"idLivro": "978-85-01-00003-3", "titulo": "Álgebra Linear", "autor": "Howard Anton, Chris Rorres", "editora": "Bookman", "codigoCutter": "C02", "estanteId": "E2"},
    {"idLivro": "978-85-01-00004-4", "titulo": "Álgebra Moderna", "autor": "Paulo Winterle", "editora": "Pearson", "codigoCutter": "C02", "estanteId": "E2"},
    
    # Estante E3 (códigos C03) - Geometria
    {"idLivro": "978-85-01-00005-5", "titulo": "Geometria Analítica", "autor": "Alfredo Steinbruch, Paulo Winterle", "editora": "Pearson", "codigoCutter": "C03", "estanteId": "E3"},
    {"idLivro": "978-85-01-00006-6", "titulo": "Geometria Diferencial", "autor": "Manfredo do Carmo", "editora": "SBM", "codigoCutter": "C03", "estanteId": "E3"},
    
    # Estante E4 (códigos C04) - Física Mecânica
    {"idLivro": "978-85-01-00007-7", "titulo": "Física I - Mecânica", "autor": "Resnick, Halliday, Krane", "editora": "LTC", "codigoCutter": "C04", "estanteId": "E4"},
    {"idLivro": "978-85-01-00008-8", "titulo": "Mecânica Clássica", "autor": "Herbert Goldstein", "editora": "Addison Wesley", "codigoCutter": "C04", "estanteId": "E4"},
    
    # Estante E5 (códigos C05) - Física Termodinâmica
    {"idLivro": "978-85-01-00009-9", "titulo": "Física II - Termodinâmica", "autor": "Resnick, Halliday, Krane", "editora": "LTC", "codigoCutter": "C05", "estanteId": "E5"},
    {"idLivro": "978-85-01-00010-0", "titulo": "Termodinâmica", "autor": "Yunus Cengel, Michael Boles", "editora": "McGraw Hill", "codigoCutter": "C05", "estanteId": "E5"},
    
    # Estante E6 (códigos C06) - Eletromagnetismo
    {"idLivro": "978-85-01-00011-1", "titulo": "Física III - Eletromagnetismo", "autor": "Resnick, Halliday, Krane", "editora": "LTC", "codigoCutter": "C06", "estanteId": "E6"},
    {"idLivro": "978-85-01-00012-2", "titulo": "Eletrodinâmica Clássica", "autor": "David Griffiths", "editora": "Pearson", "codigoCutter": "C06", "estanteId": "E6"},
    
    # Estante E7 (códigos C07) - Química
    {"idLivro": "978-85-01-00013-3", "titulo": "Química Geral", "autor": "John McMurry, Robert Fay", "editora": "Cengage Learning", "codigoCutter": "C07", "estanteId": "E7"},
    {"idLivro": "978-85-01-00014-4", "titulo": "Química Orgânica", "autor": "John McMurry", "editora": "Cengage Learning", "codigoCutter": "C07", "estanteId": "E7"},
    
    # Estante E8 (códigos C08) - Programação
    {"idLivro": "978-85-01-00015-5", "titulo": "Programação em Python", "autor": "Mark Lutz", "editora": "Novatec", "codigoCutter": "C08", "estanteId": "E8"},
    {"idLivro": "978-85-01-00016-6", "titulo": "Python Fluente", "autor": "Luciano Ramalho", "editora": "Novatec", "codigoCutter": "C08", "estanteId": "E8"},
    
    # Estante E9 (códigos C09) - Estruturas de Dados
    {"idLivro": "978-85-01-00017-7", "titulo": "Estruturas de Dados e Algoritmos", "autor": "Michael Goodrich, Roberto Tamassia", "editora": "Bookman", "codigoCutter": "C09", "estanteId": "E9"},
    {"idLivro": "978-85-01-00018-8", "titulo": "Algoritmos - Teoria e Prática", "autor": "Thomas Cormen", "editora": "Campus", "codigoCutter": "C09", "estanteId": "E9"},
    
    # Estante E10 (códigos C10) - Banco de Dados
    {"idLivro": "978-85-01-00019-9", "titulo": "Sistemas de Banco de Dados", "autor": "Ramez Elmasri, Shamkant Navathe", "editora": "Pearson", "codigoCutter": "C10", "estanteId": "E10"},
    {"idLivro": "978-85-01-00020-0", "titulo": "Projeto de Banco de Dados", "autor": "Carlos Heuser", "editora": "Sagra Luzzatto", "codigoCutter": "C10", "estanteId": "E10"},
    
    # Estante E11 (códigos C11) - Redes
    {"idLivro": "978-85-01-00021-1", "titulo": "Redes de Computadores", "autor": "Andrew Tanenbaum, David Wetherall", "editora": "Pearson", "codigoCutter": "C11", "estanteId": "E11"},
    {"idLivro": "978-85-01-00022-2", "titulo": "Redes de Computadores e a Internet", "autor": "James Kurose, Keith Ross", "editora": "Pearson", "codigoCutter": "C11", "estanteId": "E11"},
    
    # Estante E12 (códigos C12) - Engenharia de Software
    {"idLivro": "978-85-01-00023-3", "titulo": "Engenharia de Software", "autor": "Ian Sommerville", "editora": "Pearson", "codigoCutter": "C12", "estanteId": "E12"},
    {"idLivro": "978-85-01-00024-4", "titulo": "Código Limpo", "autor": "Robert Martin", "editora": "Alta Books", "codigoCutter": "C12", "estanteId": "E12"},
]

def popular_livros():
    db: Session = SessionLocal()
    
    # Primeiro, deleta todos os livros existentes
    print("🗑️ Deletando livros existentes...")
    db.query(LivroORM).delete()
    
    # Agora adiciona os novos livros com autor
    print("📚 Adicionando novos livros com campo autor...")
    for livro in livros_exemplo:
        db.add(LivroORM(**livro))
    
    db.commit()
    db.close()
    print(f"✅ {len(livros_exemplo)} livros inseridos com sucesso!")

if __name__ == "__main__":
    popular_livros()
