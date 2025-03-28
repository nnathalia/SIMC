from django.apps import AppConfig
import threading
from esp_app import coletar_dados as coletar

class EstacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estacao'

    def ready(self):
        """Inicia a coleta de dados do ESP32 em uma thread separada ao iniciar o Django"""
        thread = threading.Thread(target=coletar.coletar_dados_periodicamente, daemon=True)
        thread.start()