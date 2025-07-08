# main.py
# Arquivo principal da aplicação FastAPI
# Aqui será inicializado o app, incluídas as rotas e configurados os middlewares.

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db.init_db import init_db
from routes.beacons import router as beacons_router
from routes.estantes import router as estantes_router
from routes.livros import router as livros_router
from routes.instancias import router as instancias_router
from routes.painel import router as painel_router
from routes.home import router as home_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configuração de CORS para permitir acesso do frontend e apps na rede local
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"  # Libera para qualquer origem (útil para testes em rede local/app mobile)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

init_db()  # Cria as tabelas no banco ao iniciar o app

app.include_router(home_router)  # Página inicial (/)
app.include_router(beacons_router)
app.include_router(estantes_router)
app.include_router(livros_router)
app.include_router(instancias_router)
app.include_router(painel_router)
