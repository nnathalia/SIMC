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
from .data import COLABORADORES, TECNOLOGIAS

def index(request):

    context = {
        "colaboradores" : COLABORADORES,
        "tecnologias" : TECNOLOGIAS
    }
    
    return render(request, 'index.html', context)

@login_required(redirect_field_name= 'login')
def dashboard(request):
    medicao = Medicao.objects.order_by('-data_hora').first()
    descricao = get_descricao(request)
    print(f"DESCRIÇAO TEMPO HOJE: {descricao}")
    previsao = get_previsao(request)
    """"
        CALCULANDO 
        Sensação Térmica = 33 + (10 ∙ √v + 10,45 - velocidade do vento) ∙ ((Temperatura - 33)) / 22
        """
    """vt = medicao.velocidade_vento / 3.6  # km/h -> m/s <- converte um m/s caso esteja recebendo em km/h"""
    vt = medicao.velocidade_vento   # em m/s
    t = medicao.temperatura         # em °C

    # Fórmula de sensação térmica (Steadman)
    sensacao_termica = 33 + (10 * (vt ** 0.5) + 10.45 - vt) * ((t - 33) / 22)
    
    icone_hoje = None
    if medicao:
        icone_hoje = escolher_icone(medicao.pluviometro)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not medicao:
            return JsonResponse({'error': 'nenhuma medição encontrada'}, status=404)
        
        data = {
            'temperatura': medicao.temperatura,
            'luminosidade': medicao.luminosidade,
            'umidade_ar': medicao.umidade_ar,
            'umidade_solo': medicao.umidade_solo,
            'pluviometro': medicao.pluviometro,
            'direcao_vento': medicao.direcao_vento,
            'velocidade_vento': medicao.velocidade_vento,
            'uv': medicao.uv,
            'ultima_atualizacao': medicao.data_hora.strftime('%d/%m/%Y %H:%M:%S'),
            'previsao' : previsao,
            'sensacao_termica': sensacao_termica
        }
        

        print(f"Sensação térmica: {sensacao_termica:.2f} °C")
        print(medicao.data_hora)
        print(medicao.temperatura)
        print(medicao.umidade_ar)
        print(medicao.umidade_solo)
        print(medicao.umidade_solo)
        print(medicao.pluviometro)
        print(medicao.direcao_vento)
        print(medicao.velocidade_vento)
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
        
        media_pluviometro = (
            Medicao.objects
            .filter(data_hora__date=dia)
            .aggregate(media_pluviometro=Avg('pluviometro'))
            .get('media_pluviometro')
        )
         
        dias_passados.append({
            'dia': dia,
            'media': round(media, 1) if media else None,
            'icone': escolher_icone(media_pluviometro)
        })
        
        context = {
            'medicao': medicao,
            'ultima_atualizacao' : medicao.data_hora if medicao else None,
            'previsao' : previsao,
            'dias_passados': dias_passados,
            'descricao_tempo' : descricao,
            'icone_hoje' : icone_hoje,
            'sensacao_termica': round(sensacao_termica) if medicao else None,
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
        pluviometro=Avg("pluviometro"),
        uv=Avg("uv"),
    )

    # médias da semana (últimos 7 dias)
    inicio_semana = hoje - timedelta(days=7)
    medias_semana = Medicao.objects.filter(data_hora__date__gte=inicio_semana).aggregate(
        temp=Avg("temperatura"),
        lum=Avg("luminosidade"),
        solo=Avg("umidade_solo"),
        ar=Avg("umidade_ar"),
        pluviometro=Avg("pluviometro"),
        uv=Avg("uv"),
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


