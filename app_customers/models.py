from django.db import models
from django.utils import timezone

class Customer(models.Model):
    external_id = models.CharField(max_length=100, unique=True)
    status = models.PositiveIntegerField(choices=[(1, "Activo"), (2, "Inactivo")], default=1)
    score = models.FloatField()
    preapproved_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.external_id