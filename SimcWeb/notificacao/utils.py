# notificacoes/utils.py
from medicao.models import Medicao
from notificacao.models import Notificacao
from django.utils import timezone

def verificar_mudancas_drasticas():
    medicoes = Medicao.objects.order_by('-data_hora')

    if medicoes.count() < 2:
        return  # precisa de pelo menos duas medições para comparar

    atual = medicoes[0]
    anterior = medicoes[1]

    notificacoes = []

    # Exemplo de thresholds (você pode ajustar):
    if abs(atual.temperatura - anterior.temperatura) > 5:
        notificacoes.append(Notificacao(
            title="Variação brusca de temperatura",
            message=f"A temperatura mudou de {anterior.temperatura:.1f}°C para {atual.temperatura:.1f}°C.",
            icon="fa-solid fa-temperature-high",
            medicao=atual
        ))

    if abs(atual.velocidade_vento - anterior.velocidade_vento) > 10:
        notificacoes.append(Notificacao(
            title="Aumento súbito de ventos",
            message=f"A velocidade do vento subiu para {atual.velocidade_vento:.1f} km/h.",
            icon="fa-solid fa-wind",
            medicao=atual
        ))

    if abs(atual.uv - anterior.uv) > 2:
        notificacoes.append(Notificacao(
            title="Índice UV perigoso",
            message=f"O índice UV aumentou para {atual.uv:.1f}. Evite exposição direta ao sol.",
            icon="fa-solid fa-sun",
            medicao=atual
        ))

    # Salva todas as notificações geradas
    if notificacoes:
        Notificacao.objects.bulk_create(notificacoes)
