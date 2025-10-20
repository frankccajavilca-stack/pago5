from django.db import models

class Contact(models.Model):
    contact_id = models.CharField(max_length=100, unique=True)
    tags = models.JSONField(default=list)  # O usa CharField dependiendo tu uso
    custom_fields = models.JSONField(default=dict)

class WebhookLog(models.Model):
    evento = models.CharField(max_length=100)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
