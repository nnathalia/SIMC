from datetime import datetime
import locale
import requests


def get_data_atual(request):
    try: 
      #Configuração Locale para Mac/Linux
        locale.setlocale(locale.LC_TIME, 'pt-BR.UTF-8')
    except locale.Error:
        try:
          #Configuração Locale para Windows
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        except locale.Error:
                pass
        
    data_atual = datetime.now()
    data_formatada = data_atual.strftime('%A, %d de %B de %Y')
    return {'data_formatada': data_formatada.capitalize()}
  
def get_client_ip(request):
    # Pega o IP real do usuário
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def localizacao(request):
    ip = get_client_ip(request)
    
    # IP local de desenvolvimento
    if ip in ('127.0.0.1', '::1'):
        cidade = "Ji-Paraná"
        estado = "Rondônia"
        timezone = "America/Porto_Velho"
    else:
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
            data = response.json()
            cidade = data.get("city", "Desconhecido")
            estado = data.get("region", "")
            timezone = data.get("timezone")
        except Exception:
            cidade = "Desconhecido"
            estado = ""
            timezone = "UTC"

    localizacao = f"{cidade} / {estado}".strip(" /")
    return {'localizacao': localizacao,
            'cidade': cidade,
            'timezone': timezone
            }
  
