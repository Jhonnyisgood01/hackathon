from django.contrib import admin
from .models import CreditEvaluation

@admin.register(CreditEvaluation)
class RiskAdmin(admin.ModelAdmin):
    list_display = ('client', 'result', 'score_obtained', 'created_at')
    list_filter = ('result',)