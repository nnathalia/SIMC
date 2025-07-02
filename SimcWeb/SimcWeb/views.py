from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from medicao.models import Medicao, Estacao
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
        # Adicionar outros colaboradores
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
    medicao = Medicao.objects.order_by('-data_hora').first()
    return render(request, 'pages/dashboard.html', {'medicao': medicao})


@login_required(redirect_field_name= 'login')
def relatorio(request):
    return render(request, 'pages/gerador_relatorio.html')

@login_required(redirect_field_name= 'login')
def perfil(request):
    if request.method == "POST":
        nome_estacao = request.POST.get('estacao')
        
        if Estacao.objects.filter(nome_est=nome_estacao, usuario=request.user).exists():
            messages.error(request, "Você já tem uma estação com esse nome!")
            request.session['show_modal'] = True
        else:
            Estacao.objects.create(
                nome_est=nome_estacao,
                usuario=request.user
            )
            request.session['show_success_popup'] = True
        return redirect('perfil')  # ajuste para o nome real da URL

    # Se for GET, verifica se deve exibir algo
    show_modal = request.session.pop('show_modal', False)
    show_success_popup = request.session.pop('show_success_popup', False)

    context = {
        "estacao": Estacao.objects.filter(usuario=request.user),
        "show_modal": show_modal,
        "show_success_popup": show_success_popup
    }

    return render(request, 'pages/perfil.html', context)



        

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