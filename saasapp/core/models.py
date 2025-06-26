from django.db import models
from django.conf import settings
from customers.models import Tenant


class Item(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):
    """Represents the single customer record for a tenant."""

    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return self.name


class Client(models.Model):
    """Simple client record stored per tenant."""

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="tasks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return self.name
