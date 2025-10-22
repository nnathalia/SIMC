from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.shortcuts import render
from medicao.views import escolher_icone,get_descricao, get_metricas, get_dias_passados, get_medias
from medicao.metrics import METRICAS, MEDIAS_METRICAS
from medicao.models import Medicao, Estacao
from previsao.views import prev_icone, get_previsao
from django.utils import timezone
from django.db.models import Avg
from .data import COLABORADORES, TECNOLOGIAS

def index(request):

    context = {
        "colaboradores" : COLABORADORES,
        "tecnologias" : TECNOLOGIAS
    }
    
    return render(request, 'index.html', context)


@login_required(redirect_field_name='login')
def dashboard(request):
    medicao = (
        Medicao.objects
        .filter(idEstacao_fk__usuario=request.user)
        .order_by('-data_hora')
        .first()
    )

    sensacao_termica = None
    metricas = {}

    if medicao:
        vt = medicao.velocidade_vento or 0
        t = medicao.temperatura or 0
        sensacao_termica = 33 + (10 * (vt ** 0.5) + 10.45 - vt) * ((t - 33) / 22)
        metricas = get_metricas(medicao, METRICAS)

    # Obter descrição do clima com ícone seguro
    descricao_info = get_descricao(request)
    descricao_texto = descricao_info.get("descricao", "Sem dados")
    icone_hoje = descricao_info.get("icone", "bi bi-cloud")

    context = {
        "medicao": medicao,
        "ultima_atualizacao": medicao.data_hora if medicao else None,
        "previsao": get_previsao(request),
        "dias_passados": get_dias_passados(request=request),
        "descricao_tempo": descricao_texto,
        "icone_tempo": icone_hoje,
        "icone_hoje": icone_hoje,
        "sensacao_termica": round(sensacao_termica) if sensacao_termica else None,
        "metricas": metricas,
    }

    return render(request, "pages/dashboard.html", context)

@login_required(redirect_field_name="login")
def relatorio(request):
    descricao_info = get_descricao(request)
    descricao_texto = descricao_info.get("descricao", "Sem dados")
    hoje = timezone.now().date()
    tipo_periodo = request.GET.get("periodo", "semana")

    medias_mes = get_medias("mes")
    medias_semana = get_medias("semana")

    datas = [('Data Inicial', 'data_inicial'), ('Data Final', 'data_final')]
    horarios = [('Hora Inicial', 'hora_inicial'), ('Hora Final', 'hora_final')]
    campos_disponiveis = {
        'temperatura': 'Temperatura',
        'umidade_ar': 'Umidade do Ar',
        'pluviometro': 'Pluviômetro',
        'luminosidade': 'Luminosidade',
        'umidade_solo': 'Umidade do Solo',
        'direcao_vento': 'Direção do Vento',
        'velocidade_vento': 'Velocidade do Vento',
        'uv': 'Índice UV'
    }

    context = {
        "medias_mes": medias_mes,
        "medias_semana": medias_semana,
        "tipo_periodo": tipo_periodo,
        "hoje": hoje,
        "media_metricas": MEDIAS_METRICAS,
        "datas": datas,
        "horarios": horarios,
        "campos_disponiveis": campos_disponiveis,
        "descricao_tempo": descricao_texto,
    }
    return render(request, "pages/gerador_relatorio.html", context)

@login_required(redirect_field_name= 'login')
def perfil(request):
    descricao_info = get_descricao(request)
    descricao_texto = descricao_info.get("descricao", "Sem dados")
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
        return redirect('perfil')  

    show_modal = request.session.pop('show_modal', False)
    show_success_popup = request.session.pop('show_success_popup', False)
    hoje = timezone.now().date()

    context = {
        "descricao_tempo": descricao_texto,
        "estacao": Estacao.objects.filter(usuario=request.user),
        "quant_estacoes": Estacao.objects.filter(usuario=request.user).count(),
        "quant_medicoes": Medicao.objects.filter(idEstacao_fk__usuario=request.user,created_at__date=hoje).count(),
        "show_modal": show_modal,
        "show_success_popup": show_success_popup
    }

    return render(request, 'pages/perfil.html', context)

@login_required(redirect_field_name= 'login')
def notificacao(request):
    descricao_info = get_descricao(request)
    descricao_texto = descricao_info.get("descricao", "Sem dados")
    
    context ={"descricao_tempo" : descricao_texto}

    return render(request, 'pages/notificacao.html', context)



def chart_data(request):
    hoje = datetime.now().date()
    mesmo_dia_semana_passada = hoje - timedelta(days=7)
    inicio = mesmo_dia_semana_passada + timedelta(days=1)
    dias = [inicio + timedelta(days=i) for i in range((hoje - inicio).days + 1)]

    nomes_dias = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo",
    }

    labels = []
    for dia in dias:
        if dia == hoje:
            labels.append("Hoje")
        else:
            labels.append(nomes_dias[dia.weekday()])

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



