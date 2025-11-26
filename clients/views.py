from rest_framework import viewsets, filters
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    """
    API Completa para gestión de Clientes.
    Permite filtrar por DNI o Apellido automáticamente.
    """
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    
    # Buscador potente: /api/clients/?search=Perez
    filter_backends = [filters.SearchFilter]
    search_fields = ['dni', 'last_name', 'first_name', 'ruc']