from django.db import models
from estacao.models import Estacao


class Usuario(models.Model):
    idUsuario = models.AutoField(primary_key=True)
    nome_user = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    senha = models.CharField(max_length=45)
    Estacao_idEstacao = models.ForeignKey(Estacao, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_user
