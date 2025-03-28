from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Estacao
from datetime import datetime

@csrf_exempt
def salvar_dados(request):
    """
    Recebe dados do ESP32 e insere no banco de dados.
    """
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        dados = json.loads(request.body)

        estacao = Estacao(
            nome_est="Estação ESP",
            latitude=0.0,
            longitude=0.0,
            altitude=dados.get("altitude", 0.0),
            status_boolean=True,
            created_at=datetime.now(),
        )
        estacao.save()

        return JsonResponse({"mensagem": "Dados salvos com sucesso"})
    
    except Exception as e:
        return JsonResponse({"erro": f"Erro ao salvar no banco: {e}"}, status=500)
