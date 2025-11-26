import random

# 1. Interfaz (El Adaptador Base)
class GovernmentAdapter:
    def consultar_identidad(self, documento):
        raise NotImplementedError("Debe implementar consultar_identidad")

# 2. Implementación RENIEC (Simulada)
class ReniecAdapter(GovernmentAdapter):
    def consultar_identidad(self, dni):
        # En una app real, aquí llamaríamos a la API SOAP de RENIEC.
        # Simulación para Hackaton:
        if len(dni) != 8 or not dni.isdigit():
            return {"success": False, "error": "DNI Inválido"}
        
        # Simulamos datos random realistas
        return {
            "success": True,
            "data": {
                "nombres": "JUAN CARLOS",
                "apellidos": "PEREZ LOPEZ",
                "direccion": "AV. UNIVERSITARIA 123 - HUANUCO",
                "estado_civil": "SOLTERO"
            }
        }

# 3. Implementación SUNAT (Simulada)
class SunatAdapter(GovernmentAdapter):
    def consultar_identidad(self, ruc):
        # Simulación de validación
        if len(ruc) != 11 or not ruc.startswith(('10', '20')):
            return {"success": False, "error": "RUC Inválido"}
        
        estado = "ACTIVO" if int(ruc[-1]) % 2 == 0 else "BAJA DE OFICIO"
        
        return {
            "success": True,
            "data": {
                "razon_social": "BODEGA EL PEREZ S.A.C.",
                "estado": estado,
                "direccion_fiscal": "JR. DOS DE MAYO 555 - HUANUCO",
                "condicion": "HABIDO"
            }
        }

# 4. Fábrica (Para usarlo fácil en las vistas)
class IntegrationFactory:
    @staticmethod
    def get_provider(tipo):
        if tipo == 'DNI':
            return ReniecAdapter()
        elif tipo == 'RUC':
            return SunatAdapter()
        else:
            raise ValueError("Tipo de documento no soportado")