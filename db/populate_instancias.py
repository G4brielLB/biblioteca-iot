# db/populate_instancias.py
"""
Script para popular o banco de dados com instâncias de livros de exemplo.
Cada livro terá 5 instâncias, com diferentes situações.
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

# Lista dos IDs de livros atuais no banco (24 livros)
livros_ids = [
    "978-85-01-00001-1", "978-85-01-00002-2", "978-85-01-00003-3", "978-85-01-00004-4",
    "978-85-01-00005-5", "978-85-01-00006-6", "978-85-01-00007-7", "978-85-01-00008-8",
    "978-85-01-00009-9", "978-85-01-00010-0", "978-85-01-00011-1", "978-85-01-00012-2",
    "978-85-01-00013-3", "978-85-01-00014-4", "978-85-01-00015-5", "978-85-01-00016-6",
    "978-85-01-00017-7", "978-85-01-00018-8", "978-85-01-00019-9", "978-85-01-00020-0",
    "978-85-01-00021-1", "978-85-01-00022-2", "978-85-01-00023-3", "978-85-01-00024-4"
]

instancias_exemplo = []
prateleiras = ["CIMA", "MEIO", "BAIXO"]

for i, idLivro in enumerate(livros_ids):
    # Determina a posição X baseada na estante (E1-E6 coluna 1, E7-E12 coluna 2)
    estante_num = (i // 2) + 1  # 2 livros por estante
    posX = 1.75 if estante_num <= 6 else 6.25
    
    for j in range(1, 6):  # 5 instâncias por livro
        idInstancia = f"{idLivro}-EX{j}"
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
            "posX": posX + 0.1 * j,  # Pequena variação na posição
            "prateleira": prateleira,
            "situacao": situacao,
            "ultimaAtualizacao": ultimaAtualizacao
        })

def popular_instancias():
    db: Session = SessionLocal()
    
    # Primeiro, deleta todas as instâncias existentes
    print("🗑️ Deletando instâncias existentes...")
    db.query(InstanciaLivroORM).delete()
    
    # Agora adiciona as novas instâncias
    print("📚 Adicionando novas instâncias...")
    for instancia in instancias_exemplo:
        db.add(InstanciaLivroORM(**instancia))
    
    db.commit()
    db.close()
    print(f"✅ {len(instancias_exemplo)} instâncias inseridas com sucesso!")

if __name__ == "__main__":
    popular_instancias()
