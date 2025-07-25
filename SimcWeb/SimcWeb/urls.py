from django.contrib import admin
from django.urls import path, include
from SimcWeb import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('gerador_relatorio/', views.relatorio, name="relatorio"),
     path('perfil/', views.perfil, name="perfil"),
    
    path("chart-data/", views.chart_data, name="chart-data"),

    path('account/', include('account.urls')),
]

