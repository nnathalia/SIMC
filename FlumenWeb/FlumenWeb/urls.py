from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.urls import path
from FlumenWeb import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('email/', views.email, name="email"),
    path('senha/', views.senha, name="senha"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('gerador_relatorio/', views.relatorio, name="relatorio"),
    
    path("chart-data/", views.chart_data, name="chart-data"),

    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

