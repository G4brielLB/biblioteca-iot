# routes/home.py
"""
Rota para a página inicial da Biblioteca IoT.
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(tags=["Home"])

@router.get("/", response_class=FileResponse)
def pagina_inicial():
    """Página inicial com menu principal da Biblioteca IoT."""
    return FileResponse("frontend/index.html")

@router.get("/emprestimo", response_class=FileResponse)
def pagina_emprestimo():
    """Página de empréstimo de livros."""
    return FileResponse("frontend/emprestimo.html")

@router.get("/devolucao", response_class=FileResponse)
def pagina_devolucao():
    """Página de devolução de livros."""
    return FileResponse("frontend/devolucao.html")
