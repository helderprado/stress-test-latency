from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from contextlib import contextmanager


# Cria a engine do SQLAlchemy, conectando-se ao banco de dados via URL definida nas variáveis de ambiente
engine = create_engine(os.environ["DATABASE_URL"])

# Configura a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a classe base para os modelos do SQLAlchemy
Base = declarative_base()


# Modelo da tabela que armazena os resultados das tarefas Celery
class TaskResult(Base):
    __tablename__ = "tb_task_results"  # Nome da tabela no banco de dados

    task_id = Column(String, primary_key=True, index=True)  # ID único da tarefa
    status = Column(String)  # Status da tarefa (ex: "PENDING", "SUCCESS", "FAILURE")
    time_spent = Column(Float)  # Tempo total da tarefa
    test_number = Column(Integer)  # Número do teste realizado


# Cria a tabela no banco de dados se ela ainda não existir
Base.metadata.create_all(bind=engine)


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
