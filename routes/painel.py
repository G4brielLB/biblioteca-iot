# routes/painel.py
"""
Rotas do painel de visualização com interface HTML.
Páginas web para visualizar e gerenciar dados da biblioteca.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from db.session import get_db
from models.livro import LivroORM
import os

router = APIRouter(prefix="/painel", tags=["Painel de Visualização"])

@router.get("/livros", response_class=HTMLResponse)
async def painel_livros(request: Request):
    """
    Página HTML para visualizar todos os livros com busca e ordenação.
    """
    html_path = os.path.join("frontend", "livros.html")
    return FileResponse(html_path, media_type="text/html")

@router.get("/livros/{idLivro}", response_class=HTMLResponse)
async def painel_livro_detalhes(
    idLivro: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Página HTML para visualizar detalhes de um livro específico e suas instâncias.
    """
    # Verificar se o livro existe
    livro = db.query(LivroORM).filter(LivroORM.idLivro == idLivro).first()
    
    if not livro:
        return FileResponse(
            os.path.join("frontend", "livro-detalhes.html"), 
            media_type="text/html", 
            status_code=404
        )
    
    # Retornar página de detalhes
    html_path = os.path.join("frontend", "livro-detalhes.html")
    return FileResponse(html_path, media_type="text/html")