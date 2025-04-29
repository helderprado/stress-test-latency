from fastapi import APIRouter  # Importa APIRouter para definir rotas no FastAPI
from celery.result import (
    AsyncResult,
)  # Permite obter o status de uma tarefa Celery assíncrona
from app.api.dto import CeleryTaskOutputDto  # DTO para padronizar a resposta da API
from app.celery.worker import celery  # Importa a instância do Celery
from app.celery.tasks import (
    task_with_high_latency_and_full_core_usage,
)  # Importa a tarefa Celery que será executada
from datetime import datetime

# Define um roteador para o "Cenário 2", agrupando suas rotas sob o prefixo "/case_2"
router = APIRouter(prefix="/case_2", tags=["Cenário 2"])


# Endpoint para iniciar uma tarefa Celery e retornar seu ID
@router.post("/start-task")
def start_task():
    """
    Dispara uma tarefa Celery de forma assíncrona.

    - A tarefa será executada com uma latência simulada.
    - O ID da tarefa é retornado para que seu status possa ser monitorado posteriormente.

    Retorno:
        - dict: Contém o ID da tarefa para consulta posterior.
    """
    task = task_with_high_latency_and_full_core_usage.delay(
        enqueued_time=datetime.utcnow().isoformat()
    )  # Dispara a tarefa Celery em segundo plano
    return {"task_id": task.id}  # Retorna o ID da tarefa para rastreamento


# Endpoint para verificar o status de uma tarefa Celery
@router.get("/task-status/{task_id}")
def task_status(task_id: str):
    """
    Obtém o status de uma tarefa Celery assíncrona.

    - O usuário fornece o ID da tarefa para verificar se está pendente, em execução, concluída ou falhou.
    - Caso haja informações adicionais sobre a execução, elas também serão retornadas.

    Parâmetros:
        - task_id (str): ID da tarefa Celery que queremos verificar.

    Retorno:
        - Objeto CeleryTaskOutputDto contendo:
            - state: Estado atual da tarefa (PENDING, STARTED, SUCCESS, FAILURE, etc.).
            - output: Informação adicional sobre a tarefa, caso disponível.
    """
    task_result = AsyncResult(task_id, app=celery)  # Obtém o status da tarefa pelo ID
    return CeleryTaskOutputDto(
        state=task_result.state, output=task_result.info
    )  # Retorna status e informações
