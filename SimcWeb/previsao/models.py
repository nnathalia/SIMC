from django.db import models
from estacao.models import Estacao

class Previsao(models.Model):
    id = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField()
    data_hora_inicio = models.DateTimeField()
    data_hora_final = models.DateTimeField()
    temperatura_max = models.FloatField()
    temperatura_min = models.FloatField()
    luminosidade = models.FloatField()
    chuva = models.FloatField()
    umidade_ar = models.FloatField()
    umidade_solo = models.FloatField()
    qualidade_ar = models.FloatField()
    PrevisaoCol = models.CharField(max_length=45)
    Estacao_idEstacao = models.ForeignKey(Estacao, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Previsão {self.idPrevisao} - {self.Estacao_idEstacao.nome_est}"


    class Meta:
        db_table = 'simc_previsao'
