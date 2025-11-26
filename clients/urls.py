from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet

# El Router crea las URLs automáticamente (GET, POST, PUT, DELETE)
router = DefaultRouter()
router.register(r'', ClientViewSet, basename='clients')

urlpatterns = [
    path('', include(router.urls)),
]