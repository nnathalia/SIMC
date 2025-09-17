from django.db import models
from estacao.models import Estacao

class Medicao(models.Model):
    id = models.AutoField(primary_key=True)
    data_hora = models.DateTimeField()
    temperatura = models.FloatField()
    umidade_ar = models.FloatField()
    umidade_solo = models.FloatField()
    luminosidade = models.FloatField()
    pluviometro = models.FloatField()
    velocidade_vento = models.FloatField()
    direcao_vento = models.FloatField()
    uv = models.FloatField()
    idEstacao_fk = models.ForeignKey(Estacao, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:  
        db_table = 'simc_medicao'
