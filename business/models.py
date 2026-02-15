from django.db import models

from users.models import User


class Business(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    owner = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="owned_business"
    )

    def __str__(self):
        return self.name