from django.db import models
from core.models import BaseModel
from clients.models import Client

class NotificationLog(BaseModel):
    TYPE_EMAIL = 'EMAIL'
    TYPE_SMS = 'SMS'
    
    TYPE_CHOICES = [
        (TYPE_EMAIL, 'Correo Electrónico'),
        (TYPE_SMS, 'Mensaje de Texto'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_EMAIL)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    is_sent = models.BooleanField(default=False)
    
    # Campo para depuración
    error_log = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.method} -> {self.client.dni}: {self.subject}"