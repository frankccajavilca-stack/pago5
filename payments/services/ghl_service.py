# payments/services/ghl_service.py

def get_confirmed_appointments():
    """
    Simula citas con tag 'pago_confirmado' desde GHL.
    En un escenario real, se haría una request a su API.
    """
    # Ejemplo simulado: normalmente esto vendría de una API GHL
    citas = [
        {"id": "ghl_001", "contact": "Juan Pérez"},
        {"id": "ghl_002", "contact": "María López"},
        {"id": "ghl_003", "contact": "Carlos Díaz"},
    ]
    return citas
