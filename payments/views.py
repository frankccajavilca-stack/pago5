from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .services.ghl_service import get_confirmed_appointments
import logging
import hmac
import hashlib

# Configurar logging
logger = logging.getLogger(__name__)

# --- Función para validar firma de webhooks ---
def validar_webhook_signature(payload, signature):
    """
    Valida que el webhook viene de una fuente confiable
    """
    if not signature:
        return False
    
    expected = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)


# --- Función de registro de errores ---
def registrar_error(evento, detalle):
    logger.error(f"[ALERTA] {evento}: {detalle}")

from django.core.mail import send_mail
from django.conf import settings

def alerta_error_sistema(evento, detalle):
    """
    Envía una alerta cuando ocurre un error grave o webhook fallido.
    """
    registrar_error(evento, detalle)
    
    try:
        send_mail(
            subject=f"⚠️ Alerta: {evento}",
            message=f"Se ha detectado un error en el sistema:\n\n{detalle}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["brunocontreras60099@gmail.com"],  # cambia por tu correo real
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Error al enviar alerta: {str(e)}")

# --- Endpoint para recibir webhooks de Mercado Pago ---
@api_view(['POST'])
def webhook_mercadopago(request):
    """Recibe notificaciones de pagos desde Mercado Pago"""
    try:
        # TEMPORAL: Desactivar validación para pruebas
        # signature = request.headers.get('X-Signature') or request.headers.get('x-signature')
        # if not validar_webhook_signature(request.body, signature):
        #     registrar_error("Webhook con firma inválida", "Intento de acceso no autorizado")
        #     return Response({"error": "Firma inválida"}, status=status.HTTP_403_FORBIDDEN)
        
        # Procesar datos del webhook
        data = request.data
        payment_id = data.get('data', {}).get('id')
        
        if not payment_id:
            return Response({"error": "ID de pago no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Aquí procesarías el pago (actualizar estado, etc.)
        logger.info(f"Webhook recibido para pago: {payment_id}")
        
        return Response({"status": "ok", "payment_id": payment_id}, status=status.HTTP_200_OK)
        
    except Exception as e:
        registrar_error("Error procesando webhook", str(e))
        alerta_error_sistema("Error en webhook de Mercado Pago", str(e))
        return Response(
            {"error": "Error procesando webhook"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# --- API: /metrics/overview ---
@api_view(['POST'])
def metrics_overview(request):
    try:
        # Totales por estado
        total_pagos = Payment.objects.count()
        pagos_aprobados = Payment.objects.filter(status='paid').count()
        pagos_rechazados = Payment.objects.filter(status='failed').count()
        pagos_pendientes = Payment.objects.filter(status='pending').count()

        # Citas confirmadas en GHL (si no existe conexión real, simula)
        try:
            citas_confirmadas = get_confirmed_appointments()
            citas_confirmadas_count = len(citas_confirmadas)
        except Exception as e:
            citas_confirmadas_count = 0
            registrar_error("Error obteniendo citas confirmadas", str(e))

        # Armar respuesta JSON
        data = {
            "total_pagos": total_pagos,
            "pagos_aprobados": pagos_aprobados,
            "pagos_rechazados": pagos_rechazados,
            "pagos_pendientes": pagos_pendientes,
            "citas_pago_confirmado": citas_confirmadas_count,
            "timestamp": timezone.now(),
        }

        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        registrar_error("Error general en /metrics/overview", str(e))
        alerta_error_sistema("Error en /metrics/overview", str(e))

        return Response(
            {"error": "No se pudieron obtener las métricas."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# --- Vista para el dashboard HTML ---
def metrics_dashboard(request):
    """
    Renderiza el panel visual (metrics.html)
    """
    return render(request, "metrics.html")
