from abc import ABC, abstractmethod

# 1. LA INTERFAZ (Contrato)
class RiskRule(ABC):
    @abstractmethod
    def evaluate(self, client) -> int:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

# 2. REGLAS CONCRETAS (Estrategias)

class BlacklistRule(RiskRule):
    """Si está en lista negra, castigo máximo."""
    name = "Lista Negra Interna"
    
    def evaluate(self, client) -> int:
        if client.is_blacklisted:
            return -1000 # Muerte súbita
        return 0

class CentralRiesgoRule(RiskRule):
    """Evalúa calificación en Equifax/Sentinel."""
    name = "Central de Riesgos"

    def evaluate(self, client) -> int:
        if client.risk_rating == 'NORMAL':
            return 30
        elif client.risk_rating == 'CPP':
            return 0
        else: # PERDIDA
            return -100

class IncomeRule(RiskRule):
    """Más ingresos = Mejor capacidad de pago."""
    name = "Capacidad de Ingresos"

    def evaluate(self, client) -> int:
        ingreso = client.monthly_income or 0
        if ingreso > 5000:
            return 40
        elif ingreso > 2000:
            return 20
        elif ingreso > 900: # Sueldo mínimo aprox
            return 10
        return 0

# 3. EL MOTOR (Engine)
class CreditScoringEngine:
    def __init__(self):
        # Aquí "enchufamos" las reglas que queremos usar hoy
        self.rules = [
            BlacklistRule(),
            CentralRiesgoRule(),
            IncomeRule(),
            # ¿Quieres meter IA? Aquí crearías una "GeminiRiskRule"
        ]

    def process_client(self, client):
        total_score = 0
        breakdown = {}

        # Ejecutar todas las reglas
        for rule in self.rules:
            points = rule.evaluate(client)
            total_score += points
            breakdown[rule.name] = points

        # Decisión final (Matemática simple para la Demo)
        if total_score >= 50:
            status = 'APROBADO'
            # Sugerimos préstamo de 3 veces su sueldo
            amount = (client.monthly_income or 0) * 3 
        elif total_score >= 10:
            status = 'REVISION_MANUAL'
            amount = (client.monthly_income or 0) * 1
        else:
            status = 'RECHAZADO'
            amount = 0

        return {
            "score": total_score,
            "status": status,
            "amount": amount,
            "breakdown": breakdown
        }