# SaaSDjangoMultitenant

This repository contains a minimal Django project configured for multi-tenant applications using the [`django-tenants`](https://github.com/django-tenants/django-tenants) package. It can be used as a starting point for building a Software‑as‑a‑Service (SaaS) product where each tenant has its own PostgreSQL schema.

## Prerequisites

- **Python**: 3.12 or later
- **PostgreSQL**: A running PostgreSQL instance with a superuser available for schema creation

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the project requirements:

   ```bash
   pip install -r tenantsaas/requirements.txt
   ```

3. Configure your database settings in `tenantsaas/tenantsaas/settings.py`. For a typical local setup you will need a database name, user and password with permissions to create schemas.

## Running the application

From the `tenantsaas` directory run the initial migrations and start the development server:

```bash
cd tenantsaas
python manage.py migrate_schemas --shared
python manage.py runserver
```

The project uses `django-tenants` which automatically sets the correct database schema based on the incoming host name.

## Managing new tenants

1. Create a tenant model instance (for example `Client`) and an associated domain (`Domain`). Saving a tenant automatically creates its schema.
2. After creating the tenant, run migrations for that tenant using `migrate_schemas`:

   ```bash
   python manage.py migrate_schemas --tenant <schema_name>
   ```

This command will apply any pending migrations to the new tenant’s schema.

For more details see the `django-tenants` documentation.
