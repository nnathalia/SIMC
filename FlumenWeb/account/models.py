from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    nome = models.CharField(max_length=255)
    email_reserva = models.EmailField(blank=True, null=True)
    cadastro_nacional = models.CharField(max_length=20, blank=True, null=True)
    contato = models.CharField(max_length=20)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nome']

    class Meta:
        db_table = 'flu_usuario'


class Endereco(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='endereco')
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)

    class Meta:
        db_table = 'flu_endereco'

