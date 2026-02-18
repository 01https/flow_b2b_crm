from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","business", "img", "name", "price", "description"]
        read_only_fields = ["business"]
