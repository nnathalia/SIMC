from django.db import models
from django.conf import settings

class Estacao(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='estacao',
    )
    nome_est = models.CharField(max_length=45)
    """Esse campo é o identificador do Arduino, que você grava no 
    firmware ou mostra via Serial para o usuário cadastrar no sistema."""
    identificador = models.CharField(max_length=50, unique=True, blank=True, null=True)  # 🔹 novo campo
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    altitude = models.FloatField(blank=True, null=True)
    status_boolean = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome_est

    class Meta:
        db_table = 'simc_estacao'
