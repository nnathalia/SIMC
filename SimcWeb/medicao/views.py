from django.conf import settings
from django.shortcuts import render
from django.db.models import Avg
from django.utils import timezone
from datetime import datetime, timedelta, timezone as tz
from SimcWeb.context_processors import localizacao
from .models import Medicao
from .metrics import METRICAS
import requests
from django.http import JsonResponse

def get_descricao(request):
    city_name = localizacao(request)['cidade']
    api_key = settings.API_KEY
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&lang=pt_br&units=metric"

    resp = requests.get(url)
    if resp.status_code != 200:
        return {"descricao": "Não foi possível obter a descrição do clima.", "icone": "bi bi-cloud"}

    data = resp.json()
    hoje = datetime.now(tz.utc).date()

    descricoes = [
        item["weather"][0]["description"].capitalize()
        for item in data.get("list", [])
        if datetime.fromtimestamp(item["dt"], tz=tz.utc).date() == hoje
    ]

    if descricoes:
        descricao_final = max(set(descricoes), key=descricoes.count)
        icone = escolher_icone_descricao(descricao_final)
        return {"descricao": descricao_final, "icone": icone}
    else:
        return {"descricao": "Sem dados para hoje.", "icone": "bi bi-cloud"}

    
    


def atualizar_medicao(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuário não autenticado'}, status=403)

    medicao = (
        Medicao.objects
        .filter(idEstacao_fk__usuario=request.user)
        .order_by('-data_hora')
        .first()
    )

    if not medicao:
        return JsonResponse({'error': 'Nenhuma medição encontrada'}, status=404)

    # Cálculo da sensação térmica
    vt = medicao.velocidade_vento or 0
    t = medicao.temperatura or 0
    sensacao_termica = 33 + (10 * (vt ** 0.5) + 10.45 - vt) * ((t - 33) / 22)

    # Métricas formatadas
    metricas = get_metricas(medicao, METRICAS)

    # Dados para o frontend
    dados = {
        "temperatura": round(medicao.temperatura, 0) if medicao.temperatura else "—",
        "sensacao_termica": round(sensacao_termica, 0),
        "ultima_atualizacao": medicao.data_hora.strftime("%d/%m/%Y %H:%M"),
        "metricas": metricas,
    }

    for m in metricas:
        dados[m["campo"]] = m["valor"]

    return JsonResponse(dados)



def escolher_icone(chuva):
    """Escolhe ícone baseado no valor de chuva (float)."""
    if chuva is None:
        return "bi bi-cloud"
    elif chuva > 50:
        return "bi bi-cloud-lightning-rain"
    elif chuva > 0:
        return "bi bi-cloud-drizzle"
    else:
        return "bi bi-brightness-high"


def escolher_icone_descricao(descricao):
    """Escolhe ícone baseado na descrição do clima (string)."""
    if not descricao:
        return "bi bi-cloud"
    descricao = descricao.lower()
    if "chuva" in descricao or "rain" in descricao:
        return "bi bi-cloud-drizzle"
    elif "tempestade" in descricao or "storm" in descricao:
        return "bi bi-cloud-lightning-rain"
    elif "nuvem" in descricao or "cloud" in descricao:
        return "bi bi-cloud"
    else:
        return "bi bi-brightness-high"



# 🔹 Funções que antes estavam no services.py
def get_metricas(medicao, METRICAS):
    """
    Retorna a lista de métricas já preenchida com os valores da última medição.
    Para a métrica de UV (campo 'uv'), adiciona a classificação (nivel, cor e icone).
    Para a métrica de Direção Vento (campo 'direcao_vento'), adiciona a sigla da direção em 'classificacao'.
    """
    metricas_resultado = []
    if not medicao:
        return metricas_resultado
    for m in METRICAS:
        valor = getattr(medicao, m["campo"], None)
        metrica_atualizada = {**m, "valor": valor}
        
        # Classificação específica para UV (campo 'uv')
        if m["campo"] == "uv":
            if valor is not None:
                classificacao = classificar_uv(valor)
                # Atualiza o campo 'classificacao' com o nível (para compatibilidade)
                metrica_atualizada["classificacao"] = classificacao["nivel"]
                # Adiciona cor e icone da classificação (sobrescreve se necessário)
                metrica_atualizada["cor"] = classificacao["cor"]
        
        # Classificação específica para Direção Vento (campo 'direcao_vento')
        elif m["campo"] == "direcao_vento":
            if valor is not None:
                classificacao = classificar_direcao_vento(valor)
                # Atualiza o campo 'classificacao' com a sigla (ex: 'N')
                metrica_atualizada["classificacao"] = classificacao["sigla"]
                # Opcional: Adicionar nome completo se quiser exibir mais detalhes no futuro
                # metrica_atualizada["nome_direcao"] = f"{sigla} (ex: Norte)"
        
        metricas_resultado.append(metrica_atualizada)
    return metricas_resultado



def get_dias_passados(qtd_dias=3, request=None):
    hoje = timezone.now().date()
    dias_passados = []

    city_name = localizacao(request)['cidade'] if request else None
    API_KEY = "0690b99f7ea9ac664d4e4945ebe8b5de"

    weather_data = {}
    if city_name:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&lang=pt_br&units=metric"
        resp = requests.get(url)
        if resp.status_code == 200:
            weather_data = resp.json()

    for i in range(1, qtd_dias + 1):
        dia = hoje - timedelta(days=i)

        # Média de temperatura
        media_temp = Medicao.objects.filter(data_hora__date=dia).aggregate(media_temp=Avg('temperatura')).get('media_temp')

        # Média de pluviômetro
        media_pluviometro = Medicao.objects.filter(data_hora__date=dia).aggregate(media_pluviometro=Avg('pluviometro')).get('media_pluviometro')

        chuva_media = None
        if media_pluviometro is not None:
            try:
                chuva_media = float(media_pluviometro)
            except (ValueError, TypeError):
                chuva_media = None

        # Busca descrição do OpenWeather para o dia
        descricao = None
        if weather_data:
            descricoes = [
                item["weather"][0]["description"].capitalize()
                for item in weather_data.get("list", [])
                if datetime.fromtimestamp(item["dt"], tz=tz.utc).date() == dia
            ]
            if descricoes:
                descricao = max(set(descricoes), key=descricoes.count)

        # Escolhe o ícone
        if descricao:
            icone = escolher_icone_descricao(descricao)
        else:
            icone = escolher_icone(chuva_media)

        dias_passados.append({
            "dia": dia,
            "media": round(media_temp, 1) if media_temp else None,
            "icone": icone,
            "descricao": descricao or "Sem dados",
        })

    return dias_passados




def classificar_uv(index: float) -> dict:
    if index < 3:
        return {"nivel": "Baixo", "cor": "text-success"}
    elif 3 <= index < 6:
        return {"nivel": "Moderado", "cor": "text-warning"}
    elif 6 <= index < 8:
        return {"nivel": "Alto", "cor": "text-orange"}
    elif 8 <= index < 11:
        return {"nivel": "Muito Alto", "cor": "text-danger"}
    else:
        return {"nivel": "Extremo", "cor": "text-purple"}


def classificar_direcao_vento(graus: float) -> dict:
    """
    Classifica a direção do vento em graus (0-360) para as 8 direções principais,
    retornando a sigla (ex: 'N' para Norte).
    """
    # Normaliza para 0-360
    graus = graus % 360
    if graus < 0:
        graus += 360
    if 337.5 <= graus or graus < 22.5:
        sigla = "N (Norte)"
    elif 22.5 <= graus < 67.5:
        sigla = "NE (Nordeste)"
    elif 67.5 <= graus < 112.5:
        sigla = "E (Leste)"
    elif 112.5 <= graus < 157.5:
        sigla = "SE (Sudeste)"
    elif 157.5 <= graus < 202.5:
        sigla = "S (Sul)"
    elif 202.5 <= graus < 247.5:
        sigla = "SO (Sudoeste)" 
    elif 247.5 <= graus < 292.5:
        sigla = "O (Oeste)"
    else:  # 292.5 <= graus < 337.5
        sigla = "NO (Noroeste)"  
    return {"sigla": sigla, "classificacao": sigla} 


def get_medias(periodo):
    hoje = timezone.now().date()
    if periodo == "mes":
        data_inicial = hoje - timedelta(days=30)
    else:
        data_inicial = hoje - timedelta(days=7)

    medias = Medicao.objects.filter(data_hora__date__gte=data_inicial).aggregate(
        temp=Avg("temperatura"),
        lum=Avg("luminosidade"),
        solo=Avg("umidade_solo"),
        ar=Avg("umidade_ar"),
        pluviometro=Avg("pluviometro"),
        uv=Avg("uv"),
    )
    for k, v in medias.items():
        medias[k] = v or 0
    return medias