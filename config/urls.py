from django.contrib import admin
from django.urls import path, include  # <--- AQUÍ ESTABA EL ERROR (Faltaba 'include')
from core.views import dashboard_view  # Asegúrate de tener la vista del dashboard

urlpatterns = [
    # 1. El Panel de Administración (Jazzmin)
    path('admin/', admin.site.urls),

    # 2. Tu Dashboard Ejecutivo (Visual)
    path('dashboard/', dashboard_view, name='dashboard'),

    # 3. Las APIs (Lógica Backend)
    path('api/risk/', include('credit_risk.urls')),
    
    path('api/integrations/', include('integrations.urls')),
    
    path('api/analytics/', include('analytics.urls')),
]