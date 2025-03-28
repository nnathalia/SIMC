import requests
import time
from datetime import datetime
import threading

ESP32_IP = "192.168.22.99"
DJANGO_API_URL = "http://localhost:8000/estacao/salvar_dados/"

# Variável para evitar múltiplas execuções
rodando = False

def get_esp_data():
    """Obtém dados do ESP32"""
    try:
        response = requests.get(f"http://{ESP32_IP}/dados", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao ESP32: {e}")
        return None

def calcular_media(dados_coletados):
    """Calcula a média das medições"""
    if not dados_coletados:
        return None

    media = {}
    for chave in dados_coletados[0].keys():
        valores = [d[chave] for d in dados_coletados if chave in d]
        media[chave] = sum(valores) / len(valores) if valores else 0

    return media

def coletar_dados_periodicamente():
    """Coleta dados a cada 10 minutos e envia média a cada hora"""
    global rodando
    if rodando:
        return  # Evita iniciar múltiplas vezes
    rodando = True

    dados_acumulados = []
    
    while True:
        dados = get_esp_data()
        if dados:
            dados_acumulados.append(dados)
            print(f"Dados coletados: {dados}")

        if len(dados_acumulados) == 6:  # 10 min x 6 = 1 hora
            media_horaria = calcular_media(dados_acumulados)
            if media_horaria:
                media_horaria["timestamp"] = datetime.now().isoformat()
                try:
                    response = requests.post(DJANGO_API_URL, json=media_horaria)
                    response.raise_for_status()
                    print("Média horária enviada com sucesso!")
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao enviar média horária: {e}")
            
            dados_acumulados.clear()

        time.sleep(600)  # Espera 10 minutos antes da próxima coleta
