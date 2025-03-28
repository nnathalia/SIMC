import requests

ESP32_IP = "192.168.22.99"  # Defina o IP do ESP32

def get_esp_data():
    """
    Obtém os dados do ESP32 via requisição HTTP.
    Retorna um dicionário com os dados ou None em caso de erro.
    """
    try:
        response = requests.get(f"http://{ESP32_IP}/dados", timeout=5)
        response.raise_for_status()  # Levanta erro HTTP caso ocorra
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar ao ESP32: {e}")
        return None
