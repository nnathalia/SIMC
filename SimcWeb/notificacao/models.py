from django.db import models
from medicao.models import Medicao

class Notificacao(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    message = models.TextField()
    icon = models.CharField(max_length=50, default="fa-solid fa-triangle-exclamation")
    timestamp = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    medicao = models.ForeignKey(Medicao, on_delete=models.CASCADE, related_name="notificacoes")

    class Meta:
        db_table = "simc_notificacao"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.title} - {self.timestamp.strftime('%d/%m %H:%M')}"
