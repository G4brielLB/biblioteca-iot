from typing import List, Optional
from pydantic import BaseModel, Field
from models.livro import Livro
from models.instancia_livro import InstanciaLivro
from models.estante import Estante
from models.beacon import Beacon

class LivroComInstancias(BaseModel):
    livro: Livro
    instancias: List[InstanciaLivro]

class DetalhesInstancia(BaseModel):
    instancia: InstanciaLivro
    livro: Livro
    estante: Optional[Estante]
    beacons: List[Beacon]

class DevolucaoRequest(BaseModel):
    nova_posX: float = Field(..., description="Nova posição X na estante após devolução")
    nova_prateleira: str = Field(..., pattern="^(CIMA|MEIO|BAIXO)$", description="Nova prateleira (CIMA, MEIO ou BAIXO)")
