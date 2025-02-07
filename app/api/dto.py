from pydantic import BaseModel
from typing import Optional


# Define um modelo de saída para representar o status de uma tarefa Celery
class CeleryTaskOutputDto(BaseModel):
    state: str  # Estado atual da tarefa (ex: "PENDING", "SUCCESS", "FAILURE")
    output: Optional[str] = (
        None  # Resultado da tarefa (pode ser None se ainda não estiver concluída)
    )
