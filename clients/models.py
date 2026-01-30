from django.db import models


class Client(models.Model):
    """Model of clients for Kanban, Clients(Table), Client Details"""
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In Progress"
        DONE = "done", "Done"

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
        )
    email = models.EmailField(blank=True, unique=True)
    phone = models.CharField(max_length=20, unique=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name}, {self.last_name}"
