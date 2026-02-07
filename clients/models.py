from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from business.models import Business
from products.models import Product


class Client(SafeDeleteModel):
    """Model of clients for Kanban, Clients(Table), Client Details"""

    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    _safedelete_policy = SOFT_DELETE

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
        )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    business = models.ForeignKey(Business, on_delete=models.PROTECT, related_name="clients")
    products = models.ManyToManyField(
        Product,
        related_name="clients",
        blank=True
        )

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"
