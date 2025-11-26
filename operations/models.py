from django.db import models
from django.utils import timezone
from core.models import BaseModel
from clients.models import Client

class Loan(BaseModel):
    """
    Representa un Crédito Activo en el Banco.
    Se crea solo cuando el análisis de riesgo (Mod 4) fue aprobado.
    """
    STATUS_PENDING = 'PENDIENTE'    # Aprobado por riesgo, falta firma
    STATUS_ACTIVE = 'ACTIVO'        # Dinero entregado
    STATUS_PAID = 'PAGADO'          # Deuda en cero
    STATUS_DEFAULT = 'MOROSO'       # No pagó

    STATUS_CHOICES = [
        (STATUS_PENDING, '⏳ Pendiente de Desembolso'),
        (STATUS_ACTIVE, '💰 Activo / Desembolsado'),
        (STATUS_PAID, '✅ Cancelado Totalmente'),
        (STATUS_DEFAULT, '🚨 En Mora / Judicial'),
    ]

    # Datos Generales
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="loans", verbose_name="Cliente")
    code = models.CharField(max_length=20, unique=True, verbose_name="Cód. Operación") # Ej: LOAN-2023-001
    
    # Condiciones Financieras
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Monto Prestado")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0, verbose_name="Tasa Interés %")
    term_months = models.IntegerField(default=12, verbose_name="Plazo (Meses)")
    
    # Saldos (Contabilidad en tiempo real)
    start_date = models.DateField(default=timezone.now, verbose_name="Fecha Desembolso")
    due_date = models.DateField(blank=True, null=True, verbose_name="Vencimiento Final")
    
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    # Auditoría Interna
    approved_by_user_id = models.IntegerField(blank=True, null=True, verbose_name="ID Aprobador (User)")

    class Meta:
        verbose_name = "Préstamo Bancario"
        verbose_name_plural = "Cartera de Préstamos"

    def __str__(self):
        return f"{self.code} - S/ {self.amount} ({self.client.full_name})"


class Transaction(BaseModel):
    """
    Registra cada movimiento de dinero. 
    Esto simula tu 'Libro Mayor' o Blockchain simple.
    """
    TYPE_DISBURSEMENT = 'DESEMBOLSO' # Salida de dinero del banco
    TYPE_PAYMENT = 'PAGO_CUOTA'      # Entrada de dinero al banco
    
    TYPE_CHOICES = [
        (TYPE_DISBURSEMENT, 'Desembolso (Salida)'),
        (TYPE_PAYMENT, 'Pago de Cuota (Entrada)'),
    ]

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    operation_date = models.DateTimeField(default=timezone.now)
    
    # Para la factura electrónica o voucher
    trace_code = models.CharField(max_length=64, blank=True, help_text="Hash único de operación")

    def __str__(self):
        return f"{self.transaction_type} - S/ {self.amount} | Cred: {self.loan.code}"