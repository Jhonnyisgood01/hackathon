from django.db.models.signals import post_save
from django.dispatch import receiver
from credit_risk.models import CreditEvaluation # El sujeto observado
from .services import NotificationService # El servicio que ejecuta

@receiver(post_save, sender=CreditEvaluation)
def notify_evaluation_result(sender, instance, created, **kwargs):
    """
    Se ejecuta AUTOMÁTICAMENTE cada vez que se guarda una evaluación de riesgo.
    """
    if created:
        client = instance.client
        result = instance.result
        
        if result == 'APROBADO':
            asunto = "¡Felicidades! Crédito Pre-Aprobado"
            mensaje = f"Hola {client.first_name}, tu crédito por S/ {instance.suggested_amount} está listo."
        else:
            asunto = "Resultado de Evaluación Crediticia"
            mensaje = f"Hola {client.first_name}, por el momento no podemos ofrecerte el producto."

        # Disparamos la notificación
        NotificationService.send_notification(
            client=client,
            subject=asunto,
            message=mensaje,
            method='EMAIL'
        )