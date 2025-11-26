from django.urls import path
from .views import KpiDataView, ExportClientsCSV

urlpatterns = [
    path('kpis/', KpiDataView.as_view(), name='api-kpis'),
    path('exportar/clientes/', ExportClientsCSV.as_view(), name='export-clients'),
]