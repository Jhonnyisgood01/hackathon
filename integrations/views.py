from rest_framework.views import APIView
from rest_framework.response import Response
from .services import IntegrationFactory
from core.utils import custom_response

class ConsultarDocumentoView(APIView):
    """
    GET /api/integrations/consultar/?tipo=DNI&numero=12345678
    """
    def get(self, request):
        tipo = request.query_params.get('tipo', 'DNI') # DNI o RUC
        numero = request.query_params.get('numero')
        
        if not numero:
            return custom_response(success=False, message="Falta el número de documento", status_code=400)

        try:
            # Usamos el Factory (Limpio y escalable)
            provider = IntegrationFactory.get_provider(tipo)
            resultado = provider.consultar_identidad(numero)
            
            if resultado['success']:
                return custom_response(message="Consulta exitosa", data=resultado['data'])
            else:
                return custom_response(success=False, message=resultado['error'])

        except Exception as e:
            return custom_response(success=False, message=str(e), status_code=500)