import logging
from .models import NotificationLog

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Simula el envío de notificaciones. 
    En producción aquí iría Twilio o SendGrid.
    """
    
    @staticmethod
    def send_notification(client, subject, message, method='EMAIL'):
        # 1. Simulación del envío (Esto se ve en la terminal)
        print(f"📧 [ENVIANDO {method}] a {client.email} | Asunto: {subject}")
        
        success = True
        error_msg = ""
        
        # Aquí simularíamos un fallo aleatorio si quisiéramos probar resiliencia
        
        # 2. Guardar en Base de Datos (Auditoría)
        NotificationLog.objects.create(
            client=client,
            method=method,
            subject=subject,
            message=message,
            is_sent=success,
            error_log=error_msg
        )
        return success