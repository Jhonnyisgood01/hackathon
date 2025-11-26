from rest_framework.response import Response
from rest_framework import status

def custom_response(data=None, message="Operación exitosa", success=True, status_code=status.HTTP_200_OK):
    """
    Formato estándar para las respuestas del API.
    Retorna:
    {
        "success": true,
        "message": "Mensaje...",
        "data": { ... }
    }
    """
    return Response({
        "success": success,
        "message": message,
        "data": data if data is not None else {}
    }, status=status_code)