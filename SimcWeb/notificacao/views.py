
from django.shortcuts import render, redirect
from .models import Notificacao

def lista_notificacoes(request):
    notifications = Notificacao.objects.all()
    return render(request, "pages/notificacao.html", {"notifications": notifications})


def marcar_todas_como_lidas(request):
    Notificacao.objects.update(lida=True)
    return redirect("notificacoes")
