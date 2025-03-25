from django.db import models

class Estacao(models.Model):
    id = models.AutoField(primary_key=True)
    nome_est = models.CharField(max_length=45)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    status_boolean = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nome_est

    class Meta:  
        db_table = 'flu_estacao'

