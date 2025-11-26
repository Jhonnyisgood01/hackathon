from django.db import models
from core.models import BaseModel
from clients.models import Client

class CreditEvaluation(BaseModel):
    """
    Guarda el historial de cada vez que la IA o el motor evaluó a un cliente.
    """
    RESULT_APPROVED = 'APROBADO'
    RESULT_REJECTED = 'RECHAZADO'
    RESULT_REVIEW = 'REVISION_MANUAL'

    RESULT_CHOICES = [
        (RESULT_APPROVED, '✅ Aprobado'),
        (RESULT_REJECTED, '❌ Rechazado'),
        (RESULT_REVIEW, '🧐 Requiere Revisión'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="risk_evaluations")
    score_obtained = models.IntegerField(default=0, verbose_name="Puntaje Calculado")
    suggested_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Monto Sugerido")
    
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    
    # Aquí guardamos el JSON exacto de por qué ganó o perdió puntos (Ej: {"ingresos": +20, "central_riesgo": -50})
    rules_breakdown = models.TextField(default="{}", verbose_name="Detalle de Reglas")

    def __str__(self):
        return f"{self.client.dni} - {self.result} (Score: {self.score_obtained})"