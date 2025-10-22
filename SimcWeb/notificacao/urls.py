# notificacoes/urls.py
from django.urls import path
from . import views

urlpatterns = [
  path('', views.lista_notificacoes, name='notificacoes'),
  path('marcar-todas/', views.marcar_todas_como_lidas, name='marcar_todas'),
]
