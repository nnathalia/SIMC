from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


@login_required
def cadastro(request):
    return render(request, 'forms\cadastro.html')


@login_required
def senha(request):
    return render(request, 'forms\senha.html')


@login_required
def dashboard(request):
    return render(request, 'pages\dashboard.html')


@login_required
def relatorio(request):
    return render(request, 'pages\gerador_relatorio.html')
