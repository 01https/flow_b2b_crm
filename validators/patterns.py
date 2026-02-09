import re


EMAIL_PATTERN = re.compile(r'^[\w.+-]+@([\w-]+\.){1,3}[\w-]{2,}$')
PHONE_PATTERN = re.compile(r'^\+?\d{10,15}$')
NAME_PATTERN = re.compile(r"^[A-Za-z\s'-]+$")
PASSWORD_PATTERN = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9!@#$%^&*(),.?":{}|<>_\-\\[\]\\/+=~`]).{8,50}$'
)
