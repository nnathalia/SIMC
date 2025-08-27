
from django.urls import path
from . import views

urlpatterns = [
    path("gerar/", views.gerar_relatorio, name="gerar_relatorio"),
]
