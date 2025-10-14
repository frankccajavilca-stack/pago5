
from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('failed', 'Fallido'),
    ]
    
    # Identificadores
    appointment_id = models.CharField(max_length=100)
    contact_id = models.CharField(max_length=100)
    
    # Mercado Pago
    preference_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True, unique=True)
    init_point = models.URLField()
    
    # Detalles del pago
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment {self.preference_id} - {self.status}"
