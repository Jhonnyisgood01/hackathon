import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import DashboardService
from clients.models import Client
from core.utils import custom_response

# 1. API de Datos para Gráficos
class KpiDataView(APIView):
    def get(self, request):
        kpis = DashboardService.get_kpis()
        return custom_response(data=kpis, message="Datos actualizados al momento")

# 2. Descargar Reporte (Excel / CSV)
class ExportClientsCSV(APIView):
    """
    Genera un archivo .csv descargable con toda la cartera de clientes.
    """
    def get(self, request):
        # Configurar cabeceras para descarga de archivo
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_cartera_mibanco.csv"'

        writer = csv.writer(response)
        # Encabezados del Excel
        writer.writerow(['DNI', 'Cliente', 'Ingresos', 'Distrito', 'Riesgo', 'Score IA'])

        # Llenar datos
        clientes = Client.objects.all().select_related()
        for c in clientes:
            # Tratamos de buscar su última nota de crédito si existe
            score = "N/A" 
            if hasattr(c, 'risk_evaluations') and c.risk_evaluations.exists():
                score = c.risk_evaluations.last().score_obtained

            writer.writerow([
                c.dni, 
                c.full_name, 
                c.monthly_income, 
                c.district, 
                c.risk_rating,
                score
            ])

        return response