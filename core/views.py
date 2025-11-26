from django.shortcuts import render
import folium
from clients.models import Client
from credit_risk.models import CreditEvaluation
from django.db.models import Sum

def dashboard_view(request):
    """
    Vista del Panel de Control Gerencial.
    Muestra KPIs y Mapa de Calor.
    """
    # 1. KPIs Rápidos (Totales)
    total_clients = Client.objects.count()
    # Suma de todos los préstamos "Sugeridos" (Un pequeño truco de demo)
    potential_placement = CreditEvaluation.objects.filter(result='APROBADO').aggregate(Sum('suggested_amount'))['suggested_amount__sum'] or 0

    # 2. Generar Mapa (Centrado en Huánuco, Perú)
    m = folium.Map(location=[-9.9306, -76.2422], zoom_start=13)

    # 3. Poner puntos en el mapa según clientes
    clients = Client.objects.all()
    
    for client in clients:
        # Si el cliente no tiene coordenadas, ignoramos (o inventamos unas cerca para la demo)
        lat = client.latitude or -9.9306
        lon = client.longitude or -76.2422
        
        # Color del marcador según riesgo
        color = 'green' if client.risk_rating == 'NORMAL' else 'red'
        
        folium.Marker(
            [lat, lon],
            popup=f"<b>{client.full_name}</b><br>DNI: {client.dni}<br>Ingreso: S/{client.monthly_income}",
            tooltip=client.full_name,
            icon=folium.Icon(color=color, icon='user')
        ).add_to(m)

    # Convertir mapa a HTML
    map_html = m._repr_html_()

    context = {
        'total_clients': total_clients,
        'potential_placement': potential_placement,
        'map_html': map_html,
    }
    
    return render(request, 'dashboard.html', context)