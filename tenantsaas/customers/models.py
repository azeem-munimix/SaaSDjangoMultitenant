from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'customers'

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    def __str__(self):
        return self.domain
