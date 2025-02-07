from locust import HttpUser, task, between
import requests


class PerformanceTests(HttpUser):
    # Define um tempo de espera aleatório entre 5 e 10 segundos entre requisições
    wait_time = between(5, 10)

    @task(1)
    def trigger_task(self):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

        try:
            # Define o timeout de 30 segundos para a requisição
            response = self.client.post(
                "/case_1/trigger-task", headers=headers, timeout=30
            )
            # Se a requisição passar, você pode adicionar verificações de resposta, se necessário
            response.raise_for_status()  # Lança um erro se a resposta não for 2xx
        except requests.exceptions.Timeout:
            print("A requisição excedeu o tempo limite de 30 segundos")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
