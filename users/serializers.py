from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

from validators.common import (
    validate_email,
    validate_name,
    validate_password
)


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    first_name = serializers.CharField(validators=[validate_name])
    last_name = serializers.CharField(validators=[validate_name])
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
        )
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["email", "password", "password_confirm", "first_name", "last_name"]
    
    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise ValidationError({
                "password_confirm": {"type": "PASSWORD_MISMATCH"}
                })
        return data
    
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "avatar", "email", "first_name", "last_name"]
        read_only_fields = ["email"]
