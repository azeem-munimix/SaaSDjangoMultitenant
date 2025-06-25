from django_tenants.models import TenantMixin, DomainMixin
from django.db import models
from django.conf import settings


class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    auto_create_schema = True

    class Meta:
        app_label = 'customers'

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    def __str__(self):
        return self.domain


class CustomerRequest(models.Model):
    """Stores a tenant signup pending approval."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=255)
    schema_name = models.CharField(max_length=63)
    approved = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - simple string rep
        return f"{self.name} ({'approved' if self.approved else 'pending'})"
