from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Business


User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

class BusinessSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer(read_only=True)
    class Meta:
        model = Business
        fields = [
            "id",
            "owner",
            "img",
            "name",
            "type",
            "email",
            "phone",
            "description"
            ]