from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_tenants.utils import schema_context, tenant_context

from customers.models import Tenant, Domain
from core.models import Customer, Membership


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_superuser_membership(sender, instance, created, **kwargs):
    """Ensure superusers get admin membership on the main tenant."""
    if not created or not instance.is_superuser:
        return

    schema_name = 'main'
    tenant_name = 'localhost'
    domain_name = 'localhost'

    # Create tenant and domain on the public schema
    with schema_context('public'):
        tenant, created_tenant = Tenant.objects.get_or_create(
            schema_name=schema_name,
            defaults={'name': tenant_name},
        )
        if created_tenant:
            Domain.objects.create(domain=domain_name, tenant=tenant, is_primary=True)

    # Create customer and membership inside the tenant schema
    with tenant_context(tenant):
        Customer.objects.get_or_create(
            tenant=tenant,
            defaults={'name': tenant_name, 'owner': instance},
        )
        Membership.objects.get_or_create(
            user=instance,
            tenant=tenant,
            defaults={'role': Membership.ADMIN},
        )
