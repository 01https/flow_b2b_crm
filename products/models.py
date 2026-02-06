from django.db import models
from django.core.validators import MinValueValidator
from safedelete.models import SafeDeleteModel, SOFT_DELETE

from business.models import Business


class Product(SafeDeleteModel):
    """Model for Products Card"""
    
    _safedelete_policy = SOFT_DELETE
    
    img = models.ImageField(upload_to="products/")
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
        )
    description = models.TextField(blank=True)
    business = models.ForeignKey(Business, on_delete=models.PROTECT, related_name="products")
    
    def __str__(self):
        return self.name
