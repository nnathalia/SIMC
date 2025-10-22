# medicao/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from medicao.models import Medicao
from notificacao.utils import verificar_mudancas_drasticas 

@receiver(post_save, sender=Medicao)
def criar_notificacoes(sender, instance, created, **kwargs):
    if created:
        verificar_mudancas_drasticas()
