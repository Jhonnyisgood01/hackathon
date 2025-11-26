from django.urls import path
from .views import ConsultarDocumentoView

urlpatterns = [
    path('consultar/', ConsultarDocumentoView.as_view(), name='consultar-doc'),
]