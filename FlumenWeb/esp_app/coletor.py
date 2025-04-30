import threading
import time
import requests
from django.utils import timezone 
from medicao.models import Medicao
from estacao.models import Estacao

def coletar_e_salvar(ip_esp32: str, estacao_id: int):
    while True:
        try:
            response = requests.get(f"http://{ip_esp32}/dados", timeout=5)
            response.raise_for_status()
            dados = response.json()

            estacao = Estacao.objects.get(id=estacao_id)

            Medicao.objects.create(
                data_hora=timezone.now(),
                temperatura=dados.get("temperatura", 0.0),
                umidade_ar=dados.get("umidade_ar", 0.0),
                umidade_solo=dados.get("umidade_solo", 0.0),
                luminosidade=dados.get("luminosidade", 0.0),
                chuva=dados.get("nivel_agua", 0.0),
                qualidade_ar=dados.get("uv", 0.0),
                idEstacao_fk=estacao
            )
            print("Medição salva com sucesso!")

        except Exception as e:
            print(f"Erro na coleta de dados: {e}")

        time.sleep(60)  # coleta a cada 60 segundos
