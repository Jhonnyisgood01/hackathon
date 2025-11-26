from django.urls import path
from .views import EvaluateClientView

urlpatterns = [
    path('evaluate/', EvaluateClientView.as_view(), name='evaluate-client'),
]