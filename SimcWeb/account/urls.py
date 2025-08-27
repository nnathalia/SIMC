from django.urls import path
from .views import login_view, logout_view, cadastro, verificar_email, atualizar_senha, verificar_codigo

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cadastro/', cadastro, name='cadastro'),
    path('recuperar-senha-email/', verificar_email, name="email"),
    path('recuperar-senha/',atualizar_senha , name="atualizar_senha"),

    path('verificar-codigo/', verificar_codigo, name='verificar_codigo'),

]
