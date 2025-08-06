import os
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import smtplib
from email.mime.text import MIMEText
from django.template.loader import render_to_string
import secrets, string


def _gerar_token(length=6):
    caracteres = string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(length))

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')



User = get_user_model()

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('full_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        contato = request.POST.get('contato')
        email = request.POST.get('email')

        if not all([email, password, password2, nome]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'auth/cadastro.html')

        if password != password2:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'auth/cadastro.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está em uso.')
            return render(request, 'auth/cadastro.html')

        user = User.objects.create_user(
            nome=nome,
            contato=contato,
            email=email,
            password=password
        )

        messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return redirect('login')

    return render(request, 'auth/cadastro.html')


def verificar_email(request):
    email = request.POST.get('email')

    try:
        usuario = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'Este e-mail não é válido.')
        return render(request, 'auth/email.html')

    token = _gerar_token()

    usuario.senha_Token = token
    usuario.save(update_fields=["senha_Token"])

    html = render_to_string('notificacao/email.html', {'codigo': token})

    msg = MIMEText(html, "html")
    msg["Subject"] = "Código de verificação para recuperar senha"
    msg["From"] = os.getenv("EMAIL_HOST_USER")
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_TOKEN"))
        server.send_message(msg)

    return render(request, 'auth/verificador.html', {'email': email})



def atualizar_senha(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        nova_senha = request.POST.get('nova_senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not nova_senha or not confirmar_senha:
            messages.error(request, 'Preencha todos os campos.')
            return render(request, 'auth/senha.html', {'email': email})

        if nova_senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'auth/senha.html', {'email': email})

        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('email')

        usuario.set_password(nova_senha)
        usuario.senha_Token = None
        usuario.save()

        messages.success(request, 'Senha atualizada com sucesso. Faça login.')
        return redirect('login')

    return redirect('login')

def verificar_codigo(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        email = request.POST.get('email')

        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'E-mail inválido.')
            return render(request, 'auth/senha.html')

        if usuario.senha_Token == codigo:
            return render(request, 'auth/senha.html', {'email': email})
        else:
            messages.error(request, 'Código incorreto.')
            return render(request, 'auth/verificador.html', {'email': email})

    return redirect('login')