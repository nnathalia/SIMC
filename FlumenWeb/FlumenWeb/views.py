from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def cadastro(request):
    return render(request, 'forms\cadastro.html')


def senha(request):
    return render(request, 'forms\senha.html')


@login_required(redirect_field_name= 'login')
def dashboard(request):
    return render(request, 'pages\dashboard.html')


@login_required(redirect_field_name= 'login')
def relatorio(request):
    return render(request, 'pages\gerador_relatorio.html')
