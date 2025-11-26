from django.db import models
from core.models import BaseModel # Asegúrate de tener el módulo core

class Client(BaseModel):
    """
    Cliente del banco. Información base para evaluar riesgo.
    """
    # Datos Personales
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    ruc = models.CharField(max_length=11, blank=True, null=True, verbose_name="RUC")
    
    # Contacto
    phone = models.CharField(max_length=15, verbose_name="Celular")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    email = models.EmailField(blank=True, null=True)

    # Datos Financieros (Necesarios para el motor de Riesgo)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ingresos Mensuales")
    
    # Semáforo de Riesgo (NORMAL, CPP, PERDIDA)
    risk_rating = models.CharField(max_length=20, default='NORMAL', verbose_name="Calif. Central Riesgo")
    is_blacklisted = models.BooleanField(default=False, verbose_name="Lista Negra")

    # Datos Geoespaciales (Para el Dashboard/Mapa)
    district = models.CharField(max_length=100, default="Huánuco")
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.dni})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"