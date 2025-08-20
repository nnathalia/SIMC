from django.shortcuts import render

# Create your views here.
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from SimcWeb.context_processors import localizacao
from .models import Medicao
import requests
from datetime import datetime, timezone

def get_descricao(request):
        city_name = localizacao(request)['cidade']
        API_KEY = "0690b99f7ea9ac664d4e4945ebe8b5de"
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&lang=pt_br&units=metric"

        resp = requests.get(url)
        if resp.status_code != 200:
            return "Não foi possível obter a descrição do clima."

        data = resp.json()
        hoje = datetime.now(timezone.utc).date()

        descricoes = []
        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"], tz=timezone.utc).date()
            if dt == hoje:
                descricoes.append(item["weather"][0]["description"].capitalize())

        if descricoes:
            return max(set(descricoes), key=descricoes.count)
        else:
            return "Sem dados para hoje."



def escolher_icone(chuva):
    if chuva is None:
        return "bi bi-cloud"
    elif chuva > 50:  # exemplo: mm de chuva no dia
        return "bi bi-cloud-lightning-rain"
    elif chuva > 0:
        return "bi bi-cloud-drizzle"
    else:
        return "bi bi-brightness-high"  # sol

def dashboard(request):
    hoje = timezone.now().date()
    dias_passados = []

    for i in range(1, 4):  # últimos 3 dias
        dia = hoje - timedelta(days=i)

        # Média de temperatura do dia
        media_temp = (
            Medicao.objects
            .filter(data_hora__date=dia)
            .aggregate(media_temp=Avg('temperatura'))
            .get('media_temp')
        )

        # Média de chuva do dia
        media_chuva = (
            Medicao.objects
            .filter(data_hora__date=dia)
            .aggregate(media_chuva=Avg('chuva'))
            .get('media_chuva')
        )

        dias_passados.append({
            'dia': dia,
            'media': round(media_temp, 1) if media_temp else None,
            'icone': escolher_icone(media_chuva)
        })

    return render(request, 'pages/dashboard.html', {
        'dias_passados': dias_passados
    })
