# db/session.py
"""
Configuração da sessão e engine do banco de dados SQLite em memória.
Cria as tabelas automaticamente a partir dos modelos ORM.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# String de conexão para banco persistente SQLite (arquivo local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

# Cria engine do SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Cria uma classe SessionLocal para instanciar sessões do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função utilitária para obter uma sessão (usada nas rotas)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas."""
    from models.base import Base
    from models.beacon import BeaconORM
    from models.estante import EstanteORM
    from models.livro import LivroORM
    from models.instancia_livro import InstanciaLivroORM
    
    # Cria todas as tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado com todas as tabelas!")
