from .worker import celery
import time
import random
from app.api.database import get_session, TaskResult
import datetime


@celery.task(name="task_with_high_latency")
def task_with_high_latency(enqueued_time=None):
    task_id = task_with_high_latency.request.id

    # Se o tempo de enfileiramento não for passado, considera o início como agora
    if enqueued_time:
        enqueued_time = datetime.datetime.fromisoformat(enqueued_time)
    else:
        enqueued_time = datetime.datetime.utcnow()

    start_time = datetime.datetime.utcnow()

    # Calcular o tempo que a tarefa ficou na fila
    queue_wait_time = (start_time - enqueued_time).total_seconds()

    delay = random.uniform(17, 20)

    time_spent = queue_wait_time + delay  # Tempo de execução + Tempo na fila

    try:
        time.sleep(delay)

        with get_session() as session:
            task_result = TaskResult(
                task_id=task_id,
                status="SUCCESS",
                time_spent=time_spent,  # Salva o tempo total (fila + execução)
            )
            session.add(task_result)
            session.commit()
            print(
                f"Tarefa {task_id} salva no banco com sucesso. Tempo na fila: {queue_wait_time:.2f} segundos."
            )

        return f"Tarefa {task_id} concluída após {delay:.2f} segundos, com {queue_wait_time:.2f} segundos na fila."

    except Exception as e:
        with get_session() as session:
            task_result = TaskResult(
                task_id=task_id,
                status="ERROR",
                time_spent=queue_wait_time,  # Salva o tempo na fila, mesmo em caso de erro
            )
            session.add(task_result)
            session.commit()
            print(f"Erro na tarefa {task_id}: {e}")

        raise e
