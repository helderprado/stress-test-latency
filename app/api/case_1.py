from fastapi import (
    APIRouter,
    Depends,
)  # Importa APIRouter para definir rotas no FastAPI e Depends para injeção de dependências
from app.api.database import (
    get_session,
    TaskResult,
)  # Importa o gerenciador de sessão do banco e o modelo da tabela
from uuid import uuid4  # Gera IDs únicos para identificar as tarefas
import time  # Biblioteca para manipulação de tempo
import random  # Biblioteca para geração de números aleatórios
from sqlalchemy.orm import (
    Session,
)  # Importa a classe Session para manipulação do banco de dados

# Define um roteador para o "Cenário 1", agrupando suas rotas sob o prefixo "/case_1"
router = APIRouter(prefix="/case_1", tags=["Cenário 1"])


# Endpoint para simular a execução de uma tarefa e armazenar seu resultado no banco de dados
@router.post("/trigger-task")
def trigger_task(session: Session = Depends(get_session)):
    """
    Simula a execução de uma tarefa com latência e registra o resultado no banco de dados.

    - Gera um tempo de espera aleatório entre 17 e 20 segundos.
    - Após a espera, registra a conclusão da tarefa no banco com status "SUCCESS".
    - A tarefa recebe um ID único gerado via `uuid4()`.

    Parâmetros:
        - session (Session): Sessão do banco de dados injetada automaticamente pelo FastAPI.

    Retorno:
        Nenhum retorno explícito, apenas registra a tarefa no banco de dados.
    """

    delay = random.uniform(17, 20)  # Gera um tempo de espera aleatório
    time.sleep(delay)  # Simula a latência da tarefa
    task_id = str(uuid4())  # Gera um ID único para a tarefa

    with get_session() as session:

        # Cria um novo registro da tarefa no banco de dados
        task_result = TaskResult(
            task_id=task_id,  # ID único da tarefa
            status="SUCCESS",  # Define a tarefa como concluída
            time_spent=delay,  # Registra o tempo total de execução
        )

        session.add(task_result)  # Adiciona a tarefa à sessão do banco
        session.commit()  # Confirma a inserção no banco de dados

    return f"Tarefa {task_id} concluída após {delay:.2f} segundos"
