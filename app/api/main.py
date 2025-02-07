from fastapi.middleware.cors import (
    CORSMiddleware,
)  # Middleware para permitir requisições CORS
from fastapi import (
    FastAPI,
)  # Framework para criar APIs web em Python
from app.api import case_1, case_2

# Criação da aplicação FastAPI
app = FastAPI()

# Define a lista de origens permitidas para requisições CORS
origins = [
    "*"
]  # "*" permite requisições de qualquer origem (não recomendado para produção)

# Adiciona o middleware CORS à aplicação
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Define quais origens podem acessar a API
    allow_credentials=True,  # Permite o envio de credenciais (cookies, headers de autenticação, etc.)
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos na requisição
)


# Rota para verificação de saúde da aplicação
@app.get("/healthz")
def healthz():
    """
    Endpoint para checar se a aplicação está rodando.
    Retorna uma mensagem indicando que o serviço está ativo.
    """
    return {"message": "application alive"}


app.include_router(case_1.router)
app.include_router(case_2.router)
