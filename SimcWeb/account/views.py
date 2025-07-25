from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

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


def email(request):
    return render(request, 'auth/email.html')


def senha(request):
    return render(request, 'auth/senha.html')
