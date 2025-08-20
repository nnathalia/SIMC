from collections import defaultdict
from datetime import datetime, timedelta, timezone
import locale
import requests
from SimcWeb.context_processors import localizacao


def get_previsao(request):
    city_name = localizacao(request)['cidade']
    print(city_name)
    API_KEY = "0690b99f7ea9ac664d4e4945ebe8b5de"
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&lang=pt_br&units=metric"
    
    resp = requests.get(url)
    if resp.status_code != 200:
        return []

    data = resp.json()
    forecast_data = defaultdict(list)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
    for item in data["list"]:
        dt = datetime.fromtimestamp(item["dt"], tz=timezone.utc).date()
        if dt >= tomorrow:
            forecast_data[dt].append(item)

    forecast_list = []
    for i, (date_only, entries) in enumerate(sorted(forecast_data.items())[:4]):
        temps = [e["main"]["temp"] for e in entries]
        descriptions = [e["weather"][0]["description"].capitalize() for e in entries]

        locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
        if i == 0:
            dia_str = "Amanhã"
        else:
            dia_str = date_only.strftime("%A").capitalize()  
        
        forecast_list.append({
            "dia": dia_str,
            "temp_min": min(temps),
            "temp_max": max(temps),
            "descricao": max(set(descriptions), key=descriptions.count)
        })
    return forecast_list
