# New Multi-Tenant Django Project

Fresh setup for a multi-tenant SaaS using `django-tenants`.
See `saasapp/README.md` for details.

## Local Docker Setup

Build and run the stack using docker compose:

```bash
docker-compose up --build
```

The application will be available on `http://localhost` and will read
configuration from the provided `.env` file.
