# db/init_db.py
"""
Inicializa as tabelas do banco de dados a partir dos modelos ORM.
Deve ser importado e executado no início da aplicação.
"""
from db.session import engine
from models.beacon import Base as BeaconBase
from models.estante import Base as EstanteBase
from models.livro import Base as LivroBase
from models.instancia_livro import Base as InstanciaLivroBase

# Cria todas as tabelas (se não existirem)
def init_db():
    BeaconBase.metadata.create_all(bind=engine)
    EstanteBase.metadata.create_all(bind=engine)
    LivroBase.metadata.create_all(bind=engine)
    InstanciaLivroBase.metadata.create_all(bind=engine)
