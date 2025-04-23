from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
import random

def index(request):
    colaboradores_context = [
        {
            "nome": "Nathalia Mariano",
            "funcao": "Frontend",
            "foto": "img/colaboradores/nathalia.jpeg",
            "linkedin": "https://www.linkedin.com/in/nnathallia/"
        },
        {
            "nome": "Filipe Maciel",
            "funcao": "Backend",
            "foto": "img/colaboradores/filipe.png",
            "linkedin": "https://www.linkedin.com/in/nnathallia/"
        },
        # Adicione os demais colaboradores
    ]

    tecnologias_context = [
        {"nome": "HTML", "link": "https://developer.mozilla.org/pt-BR/docs/Web/HTML", "img": "img/tecnologias/logo_html.svg"},
        {"nome": "CSS", "link": "https://developer.mozilla.org/pt-BR/docs/Web/CSS", "img": "img/tecnologias/logo_css.svg"},
        {"nome": "JavaScript", "link": "https://developer.mozilla.org/pt-BR/docs/Web/JavaScript", "img": "img/tecnologias/logo_javascript.svg"},
        {"nome": "Python", "link": "https://www.python.org/", "img": "img/tecnologias/logo_python.svg"},
        {"nome": "Django", "link": "https://www.djangoproject.com/", "img": "img/tecnologias/logo_django.svg"},
        {"nome": "Bootstrap", "link": "https://getbootstrap.com/", "img": "img/tecnologias/logo_bootstrap.svg"},
        {"nome": "PostgreSQL", "link": "https://www.postgresql.org/", "img": "img/tecnologias/logo_postgresql.svg"}
    ]

    
    return render(request, 'index.html', {
        "colaboradores_context": colaboradores_context,
        "tecnologias_context": tecnologias_context,
    })
    
def cadastro(request):
    return render(request, 'auth/cadastro.html')

def email(request):
    return render(request, 'auth/email.html')


def senha(request):
    return render(request, 'auth/senha.html')


@login_required(redirect_field_name= 'login')
def dashboard(request):
    return render(request, 'pages/dashboard.html')


@login_required(redirect_field_name= 'login')
def relatorio(request):
    return render(request, 'pages/gerador_relatorio.html')


def chart_data(request):
    data = {
        "labels": ["Segunda", "Terca", "Quarta", "Quinta", "Sexta"],
        "datasets": [
            {
                "label": "Temperatura",
                "data": [random.randint(10, 50) for _ in range(6)],
            }
        ],
    }
    return JsonResponse(data)





