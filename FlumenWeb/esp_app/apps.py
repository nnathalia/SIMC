from django.apps import AppConfig
import threading

class EspAppConfig(AppConfig):
    name = 'esp_app'

    def ready(self):
        from .coletor import coletar_e_salvar

        ip_esp = "192.168.100.191"  # Substitua pelo IP real do ESP32
        estacao_id = 1  # Substitua pelo ID real da estação

        t = threading.Thread(target=coletar_e_salvar, args=(ip_esp, estacao_id), daemon=True)
        t.start()
