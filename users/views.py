from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from .serializers import LoginSerializer, UserSerializer
from core.utils import custom_response # Usamos tu utilitario estándar

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user) # Crea la sesión en el servidor
            
            # Devolvemos info del usuario para que el Frontend sepa quién es
            user_data = UserSerializer(user).data
            return custom_response(
                message=f"Bienvenido {user.first_name}",
                data=user_data,
                success=True
            )
        return custom_response(message="Error de credenciales", success=False, status_code=400)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return custom_response(message="Sesión cerrada correctamente")

class MeView(APIView):
    """Devuelve los datos del usuario logueado actualmente"""
    def get(self, request):
        if not request.user.is_authenticated:
            return custom_response(message="No has iniciado sesión", success=False, status_code=401)
        
        serializer = UserSerializer(request.user)
        return custom_response(data=serializer.data)