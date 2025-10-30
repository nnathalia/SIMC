from SimcWeb.context_processors import localizacao
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import locale
import requests
from django.conf import settings

def get_previsao(request):
    city_name = localizacao(request)['cidade']
    api_key = settings.API_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&lang=pt_br&units=metric"
    
    resp = requests.get(url)
    if resp.status_code != 200:
        return []

    data = resp.json()
    forecast_data = defaultdict(list)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    try:
        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
    except locale.Error:
        locale.setlocale(locale.LC_TIME, "Portuguese_Brazil.1252")

    for item in data["list"]:
        dt = datetime.fromtimestamp(item["dt"], tz=timezone.utc).date()
        if dt >= tomorrow:
            forecast_data[dt].append(item)

    dias_semana = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo",
    }

    forecast_list = []
    for i, (date_only, entries) in enumerate(sorted(forecast_data.items())[:6]):
        temps = [e["main"]["temp"] for e in entries]
        descriptions = [e["weather"][0]["description"].capitalize() for e in entries]

        # Aqui usamos a lógica que você forneceu
        dia_str = "Amanhã" if i == 0 else dias_semana[date_only.weekday()]

        temp_min = min(temps)
        temp_max = max(temps)
        descricao = max(set(descriptions), key=descriptions.count)

        forecast_list.append({
            "dia": dia_str,
            "temp_min": temp_min,
            "temp_max": temp_max,
            "descricao": descricao,
            "icone": prev_icone(temp_min, temp_max, descricao)
        })

    return forecast_list



def prev_icone(temp_min: float, temp_max: float, descricao: str) -> str:
    if temp_min is None or temp_max is None or not descricao:
        return "bi-question-circle text-muted"

    desc = descricao.lower()

    # ícone pelo clima
    mapa_icones = {
    # Condições de céu
    "céu limpo": "bi-sun text-warning",
    "algumas nuvens": "bi-cloud-sun text-warning",
    "nuvens dispersas": "bi-cloud-sun text-warning",
    "nublado": "bi-clouds text-info",
    "nuvens quebradas": "bi-clouds text-info",

    # Clima adverso
    "chuva leve": "bi-cloud-drizzle text-info",
    "chuva moderada": "bi-cloud-rain text-primary",
    "chuva forte": "bi-cloud-rain-heavy text-primary",
    "trovoada": "bi-cloud-lightning-rain text-danger",
    "neve": "bi-snow text-primary-emphasis ",
    "neblina": "bi-cloud-fog text-primary-secondary",
    "névoa": "bi-cloud-fog text-primary-secondary",
    "garoa": "bi-cloud-drizzle text-primary-emphasis",
    }
    icone = next((icone for palavra, icone in mapa_icones.items() if palavra in desc.lower()), "bi-cloud-sun")


    return f"{icone}"
