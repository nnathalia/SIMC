from django.urls import path
from .views import salvar_dados

urlpatterns = [
    path('salvar_dados/', salvar_dados, name='salvar_dados'),
]
