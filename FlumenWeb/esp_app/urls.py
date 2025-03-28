from django.urls import path
from .views import coletar_dados_esp

urlpatterns = [
    path('coletar/', coletar_dados_esp, name='coletar_dados_esp'),
]
