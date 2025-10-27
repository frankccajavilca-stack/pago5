from django.urls import path
from .views import metrics_overview, metrics_dashboard, webhook_mercadopago

urlpatterns = [
    path('metrics/overview/', metrics_overview, name='metrics_overview'),
    path('metrics/dashboard/', metrics_dashboard, name='metrics_dashboard'),
    path('webhook/mercadopago/', webhook_mercadopago, name='webhook_mercadopago'),
]