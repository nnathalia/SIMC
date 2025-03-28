from django.http import JsonResponse
from .esp_client import get_esp_data
import requests

def coletar_dados_esp(request):
    """
    View para buscar dados do ESP32 e enviar para a API de estação.
    """
    dados = get_esp_data()
    if not dados:
        return JsonResponse({"erro": "Falha ao obter dados do ESP32"}, status=500)

    # Enviar para o app estacao
    estacao_url = "http://localhost:8000/estacao/salvar_dados/"
    try:
        response = requests.post(estacao_url, json=dados)
        response.raise_for_status()
        return JsonResponse({"mensagem": "Dados enviados com sucesso"})
    except requests.exceptions.RequestException as e:
        return JsonResponse({"erro": f"Falha ao enviar para estação: {e}"}, status=500)
