from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel  # Importamos nuestro modelo de auditoría

class User(AbstractUser, BaseModel):
    """
    Usuario personalizado para el sistema bancario.
    Reemplaza al usuario por defecto de Django.
    Agregamos DNI y Roles.
    """
    
    # Definición de ROLES (Enum)
    ADMINISTRADOR = 'ADMIN'
    ANALISTA = 'ANALISTA'   # Analista de riesgo (el que usa el Dashboard)
    CAJERO = 'CAJERO'       # Ventanilla (el que registra operaciones)
    EJECUTIVO = 'EJECUTIVO' # El que capta clientes (Leads)

    ROLE_CHOICES = [
        (ADMINISTRADOR, 'Administrador del Sistema'),
        (ANALISTA, 'Analista de Riesgos'),
        (CAJERO, 'Cajero / Ventanilla'),
        (EJECUTIVO, 'Ejecutivo de Negocios'),
    ]

    # Campos Adicionales
    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ANALISTA, verbose_name="Rol en el Banco")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Usuario del Sistema"
        verbose_name_plural = "Usuarios del Sistema"

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"