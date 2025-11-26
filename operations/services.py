from datetime import timedelta
from decimal import Decimal
from django.utils import timezone
from .models import Loan, Transaction

class OperationsService:
    
    @staticmethod
    def disburse_loan(loan_id):
        """
        Activa el préstamo: Cambia estado a ACTIVO y registra la salida de dinero.
        """
        loan = Loan.objects.get(id=loan_id)
        
        if loan.current_status != Loan.STATUS_PENDING:
            raise Exception("El préstamo ya fue desembolsado o cancelado.")
            
        # 1. Cambiar estado
        loan.current_status = Loan.STATUS_ACTIVE
        # Calcular vencimiento (simple: fecha hoy + dias del plazo)
        loan.due_date = loan.start_date + timedelta(days=loan.term_months * 30)
        loan.save()
        
        # 2. Registrar Transacción (Salida de Plata)
        Transaction.objects.create(
            loan=loan,
            transaction_type=Transaction.TYPE_DISBURSEMENT,
            amount=loan.amount,
            trace_code=f"TRX-START-{loan.code}"
        )
        
        return loan

    @staticmethod
    def register_payment(loan_id, amount):
        """
        Registra un pago de cliente.
        """
        loan = Loan.objects.get(id=loan_id)
        
        Transaction.objects.create(
            loan=loan,
            transaction_type=Transaction.TYPE_PAYMENT,
            amount=amount,
            trace_code=f"PAY-{timezone.now().timestamp()}"
        )
        # Aquí podrías agregar lógica para ver si ya pagó todo y cambiar a STATUS_PAID
        return True