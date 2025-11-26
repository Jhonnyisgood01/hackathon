from django.contrib import admin
from .models import Loan, Transaction

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ('operation_date', 'transaction_type', 'amount')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('code', 'client', 'amount', 'current_status', 'interest_rate')
    list_filter = ('current_status', 'start_date')
    search_fields = ('code', 'client__dni')
    inlines = [TransactionInline]
    
    # Botón mágico para el cajero
    actions = ['desembolsar_prestamo']

    def desembolsar_prestamo(self, request, queryset):
        # Aquí llamaríamos a tu servicio logic.py, pero por ahora lo hacemos directo
        updated = queryset.update(current_status='ACTIVO')
        self.message_user(request, f"{updated} préstamos han sido desembolsados.")
    desembolsar_prestamo.short_description = "💰 DESEMBOLSAR DINERO (Simulación)"