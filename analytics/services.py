from django.db.models import Sum, Count, Avg, Q
from operations.models import Loan
from clients.models import Client
from credit_risk.models import CreditEvaluation

class DashboardService:
    """
    Centraliza el cálculo de métricas financieras.
    """

    @staticmethod
    def get_kpis():
        # 1. Totales de Cartera
        total_desembolsado = Loan.objects.filter(current_status='ACTIVO').aggregate(Sum('amount'))['amount__sum'] or 0
        total_clientes = Client.objects.count()

        # 2. Análisis de Riesgo
        evaluaciones = CreditEvaluation.objects.all()
        tasa_aprobacion = 0
        if evaluaciones.exists():
            aprobados = evaluaciones.filter(result='APROBADO').count()
            tasa_aprobacion = round((aprobados / evaluaciones.count()) * 100, 1)

        # 3. Mora (Cartera Pesada) - Simulado si no hay datos
        # Calculamos % de clientes en riesgo alto (Perdida)
        mora_cartera = Client.objects.filter(risk_rating='PERDIDA').count()

        return {
            "colocacion_total": total_desembolsado,
            "clientes_activos": total_clientes,
            "tasa_aprobacion_ia": tasa_aprobacion, # % de aprobación de la IA
            "clientes_mora": mora_cartera
        }