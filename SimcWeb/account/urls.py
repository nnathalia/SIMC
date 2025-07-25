from django.urls import path
from .views import login_view, logout_view, cadastro, email, senha

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('email/', email, name="email"),
    path('senha/', senha, name="senha"),
]
