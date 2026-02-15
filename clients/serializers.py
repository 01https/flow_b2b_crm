from rest_framework import serializers

from .models import Client
from products.models import Product
from validators.common import (
    validate_name,
    validate_email,
    validate_phone,
    validate_comment
)
class ClientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "status",
            "comment",
            ]


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name"]


class ClientDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(validators=[validate_name])
    last_name = serializers.CharField(validators=[validate_name])
    email = serializers.EmailField(validators=[validate_email])
    phone = serializers.CharField(validators=[validate_phone])
    comment = serializers.CharField(validators=[validate_comment])
    products = ProductShortSerializer(many=True, read_only=True)
    products_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        source="products",
        write_only=True
    )
    class Meta:
        model = Client
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "status",
            "products",
            "products_ids",
            "comment",
            "business",
            ]
        read_only_fields = ["business"]