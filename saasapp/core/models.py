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


class Membership(models.Model):
    """Links a user to a tenant with a role."""

    ADMIN = "admin"
    MEMBER = "member"
    APPROVER = "approver"
    PUBLISHER = "publisher"
    RESIDENT = "resident"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (MEMBER, "Member"),
        (APPROVER, "Approver"),
        (PUBLISHER, "Publisher"),
        (RESIDENT, "Resident"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ["user", "tenant"]

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return f"{self.user.username} - {self.role}"


class FoiaRequest(models.Model):
    """Request created by a resident."""

    description = models.TextField()
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="foia_requests"
    )
    accepted = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_foia_requests",
    )

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return f"FOIA #{self.pk}"
