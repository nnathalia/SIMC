from django.contrib import admin
from django.urls import path
from FlumenWeb import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('email/', views.email, name="email"),
    path('senha/', views.senha, name="senha"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('gerador_relatorio/', views.relatorio, name="relatorio")
]

