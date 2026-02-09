from rest_framework.exceptions import ValidationError
from validators.patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    NAME_PATTERN,
    PASSWORD_PATTERN
)

from validators.errors import ErrorType


def validate_name(value: str):
    if not value or not value.strip():
        raise ValidationError({"type": ErrorType.REQUIRED})
    
    if not NAME_PATTERN.fullmatch(value):
        raise ValidationError({"type": ErrorType.INVALID})
    
    if len(value) < 2:
        raise ValidationError({"type": ErrorType.MIN_LENGTH, "min": 2})
    
    if len(value) > 50:
        raise ValidationError({"type": ErrorType.MAX_LENGTH, "max": 50})
    
    return value
    
def validate_email(value: str):
    if not value:
        raise ValidationError({"type": ErrorType.REQUIRED})
    
    if not EMAIL_PATTERN.fullmatch(value):
        raise ValidationError({"type": ErrorType.INVALID})
    
    return value

def normalize_phone(value: str):
    return "".join(c for c in value if c.isdigit() or c == "+")

def validate_phone(value: str):
    if not value:
        raise ValidationError({"type": ErrorType.REQUIRED})
    
    normalized = normalize_phone(value)
    
    if not PHONE_PATTERN.fullmatch(normalized):
        raise ValidationError({"type": ErrorType.INVALID})
    
    return normalized

def validate_password(value: str):
    if not value:
        raise ValidationError({"type": ErrorType.REQUIRED})
    
    if len(value) < 8:
        raise ValidationError({"type": ErrorType.MIN_LENGTH, "min": 8})
    
    if not PASSWORD_PATTERN.fullmatch(value):
        raise ValidationError({"type": ErrorType.INVALID})
    
    return value

def validate_comment(value: str):
    if not value:
        return

    if len(value) < 6:
        raise ValidationError({"type": ErrorType.MIN_LENGTH, "min": 6})

    if len(value) > 100:
        raise ValidationError({"type": ErrorType.MAX_LENGTH, "max": 100})
    
    return value