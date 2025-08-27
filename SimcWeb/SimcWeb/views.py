from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from medicao.views import escolher_icone,get_descricao
from medicao.models import Medicao, Estacao
from previsao.views import get_previsao
from django.utils import timezone
from django.db.models import Avg

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
    descricao = get_descricao(request)
    print(f"DESCRIÇAO TEMPO HOJE: {descricao}")
    previsao = get_previsao(request)
    
    icone_hoje = None
    if medicao:
        icone_hoje = escolher_icone(medicao.chuva)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not medicao:
            return JsonResponse({'error': 'nenhuma medição encontrada'}, status=404)
        
        data = {
            'temperatura': medicao.temperatura,
            'luminosidade': medicao.luminosidade,
            'umidade_ar': medicao.umidade_ar,
            'umidade_solo': medicao.umidade_solo,
            'chuva': medicao.chuva,
            'uv': medicao.uv,
            'ultima_atualizacao': medicao.data_hora.strftime('%d/%m/%Y %H:%M:%S'),
            'previsao' : previsao
        }
        """"
        CALCULANDO 
        Sensação Térmica = 33 + (10 ∙ √v + 10,45 - velocidade do vento) ∙ ((Temperatura - 33)) / 22
        """
        print(medicao.data_hora)
        print(medicao.temperatura)
        print(medicao.umidade_ar)
        print(medicao.umidade_solo)
        print(medicao.umidade_solo)
        print(medicao.uv)
        print(previsao)
        
        
        return JsonResponse(data)
    
    hoje = timezone.now().date()
    dias_passados = []

    for i in range(1, 4):
        dia = hoje - timedelta(days=i)
        media = (
            Medicao.objects
            .filter(data_hora__date=dia)
            .aggregate(media_temp=Avg('temperatura'))
            .get('media_temp')
        )
        
        media_chuva = (
            Medicao.objects
            .filter(data_hora__date=dia)
            .aggregate(media_chuva=Avg('chuva'))
            .get('media_chuva')
        )
         
        dias_passados.append({
            'dia': dia,
            'media': round(media, 1) if media else None,
            'icone': escolher_icone(media_chuva)
        })
        
        context = {
            'medicao': medicao,
            'ultima_atualizacao' : medicao.data_hora if medicao else None,
            'previsao' : previsao,
            'dias_passados': dias_passados,
            'descricao_tempo' : descricao,
            'icone_hoje' : icone_hoje
        }

    return render(request, 'pages/dashboard.html', context)


@login_required(redirect_field_name= 'login')
def relatorio(request):
    hoje = timezone.now().date()
    descricao = get_descricao(request)

    # médias do mês
    inicio_mes = hoje.replace(day=1)
    medias_mes = Medicao.objects.filter(data_hora__date__gte=inicio_mes).aggregate(
        temp=Avg("temperatura"),
        lum=Avg("luminosidade"),
        solo=Avg("umidade_solo"),
        ar=Avg("umidade_ar"),
        chuva=Avg("chuva"),
    )

    # médias da semana (últimos 7 dias)
    inicio_semana = hoje - timedelta(days=7)
    medias_semana = Medicao.objects.filter(data_hora__date__gte=inicio_semana).aggregate(
        temp=Avg("temperatura"),
        lum=Avg("luminosidade"),
        solo=Avg("umidade_solo"),
        ar=Avg("umidade_ar"),
        chuva=Avg("chuva"),
    )

    context = {
        "medias_mes": medias_mes,
        "medias_semana": medias_semana,
        "hoje": hoje,
        "descricao_tempo": descricao
    }
    
    return render(request, "pages/gerador_relatorio.html", context)

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
    hoje = datetime.now().date()

    # Mesmo dia da semana passada
    mesmo_dia_semana_passada = hoje - timedelta(days=7)
    # Começa no dia seguinte ao mesmo dia da semana passada
    inicio = mesmo_dia_semana_passada + timedelta(days=1)

    # Lista de dias do início até hoje
    dias = [inicio + timedelta(days=i) for i in range((hoje - inicio).days + 1)]

    labels = []
    for dia in dias:
        if dia == hoje:
            labels.append("Hoje")
        else:
            labels.append(dia.strftime('%A').capitalize())  # Segunda, Terça, etc.

    dados = []
    for dia in dias:
        media_dia = Medicao.objects.filter(
            data_hora__date=dia
        ).aggregate(media=Avg('temperatura'))['media']
        dados.append(round(media_dia, 1) if media_dia is not None else 0)
        
    if all(valor == 0 for valor in dados):
        dados = [10.5, 23.1, 25.0, 24.2, 26.3, 27.1, 40.0]

    data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Temperatura Média (°C)",
                "data": dados,
            }
        ],
    }
    return JsonResponse(data)


