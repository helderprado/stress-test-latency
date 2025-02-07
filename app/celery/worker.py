from celery import Celery
import os
from app.api.database import Base, engine

# Inicializa a instância do Celery com o nome "tasks"
# O broker é o sistema de fila (ex: Redis ou RabbitMQ) que gerencia as tarefas
# O backend armazena os resultados das tarefas (ex: banco de dados ou Redis)
celery = Celery(
    "tasks",
    broker=os.environ[
        "CELERY_BROKER_URL"
    ],  # Obtém a URL do broker a partir das variáveis de ambiente
    backend=os.environ["CELERY_BACKEND_URL"],  # Obtém a URL do backend de resultados
)

# Permite que o Celery descubra automaticamente as tarefas registradas no módulo "app.celery.tasks"
celery.autodiscover_tasks(["app.celery.tasks"])


@celery.on_after_configure.connect
def setup_database(sender, **kwargs):
    """Função chamada após o Celery ser configurado."""
    # Cria as tabelas no banco de dados caso ainda não existam
    Base.metadata.create_all(bind=engine)
