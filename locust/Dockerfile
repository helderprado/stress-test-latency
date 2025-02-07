# Usando uma imagem base oficial do Python
FROM python:3.9-slim

# Instalar dependências necessárias
RUN pip install locust

# Copiar o script de teste para dentro do contêiner
COPY ./src .
