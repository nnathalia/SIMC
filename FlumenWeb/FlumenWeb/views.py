from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'auth\login.html')
    
def cadastro(request):
    return render(request, 'auth\cadastro.html')

def email(request):
    return render(request, 'auth\email.html')

def senha(request):
    return render(request, 'auth\senha.html')

def dashboard(request):
    return render(request, 'pages\dashboard.html')

def relatorio(request):
    return render(request, 'pages\gerador_relatorio.html')









