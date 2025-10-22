from django.urls import path
from . import views

urlpatterns = [
  path('atualizar_medicao/', views.atualizar_medicao, name='atualizar_medicao'),
]
