from django.db import models

class BaseModel(models.Model):
    """
    Modelo base abstracto. NO crea una tabla en la base de datos.
    Agrega automáticamente campos de auditoría a los modelos que hereden de él.
    """
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        abstract = True  # ¡Crucial! Esto le dice a Django que no cree tabla para esto