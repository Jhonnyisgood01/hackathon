from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from clients.models import Client
from .models import CreditEvaluation
from .logic import CreditScoringEngine
from core.utils import custom_response

class EvaluateClientView(APIView):
    """
    POST /api/risk/evaluate/
    Body: { "dni": "12345678" }
    """
    def post(self, request):
        dni = request.data.get('dni')
        client = get_object_or_404(Client, dni=dni)

        # 1. Llamar al Motor
        engine = CreditScoringEngine()
        result = engine.process_client(client)

        # 2. Guardar en BD (Auditoría)
        eval_obj = CreditEvaluation.objects.create(
            client=client,
            score_obtained=result['score'],
            result=result['status'],
            suggested_amount=result['amount'],
            rules_breakdown=result['breakdown']
        )

        # 3. Responder bonito al Frontend
        return custom_response(
            message=f"Cliente evaluado: {result['status']}",
            data={
                "client": client.full_name,
                "status": result['status'],
                "score": result['score'],
                "suggested_amount": result['amount'],
                "details": result['breakdown']
            }
        )