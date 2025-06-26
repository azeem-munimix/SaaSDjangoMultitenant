# SaaS Django Multi-tenant

This project is a fresh Django skeleton configured for `django-tenants`.
It contains a `customers` app defining the tenant and domain models,
a `shared` app for globally installed models and a `core` app for
schemas that live per tenant.

## Initial Setup

Run the database migrations and create an initial tenant before using the
application.

```bash
python manage.py migrate
python manage.py create_tenant --schema_name=example --name="Example" --domain-domain=127.0.0.1
```

The domain must match the hostname you access in the browser; otherwise you will
see a "No tenant for hostname" error. You can also create a tenant through the
signup and approval flow instead of the management command.
