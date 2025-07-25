from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers import UsuarioManager


class Usuario(AbstractUser):
    username = None
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    email_reserva = models.EmailField(blank=True, null=True)
    cadastro_nacional = models.CharField(max_length=20, blank=True, null=True)
    contato = models.CharField(max_length=20, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

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

