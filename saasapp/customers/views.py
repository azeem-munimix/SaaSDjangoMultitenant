import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Tenant, Domain

@csrf_exempt
def create_customer(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed")

    try:
        data = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    name = data.get("name")
    domain = data.get("domain")
    schema_name = data.get("schema_name") or (name.lower().replace(" ", "_") if name else None)

    if not name or not domain or not schema_name:
        return HttpResponseBadRequest("name, domain and schema_name required")

    tenant = Tenant(schema_name=schema_name, name=name)
    tenant.save()  # creates the schema when auto_create_schema = True

    Domain.objects.create(domain=domain, tenant=tenant, is_primary=True)

    return JsonResponse({"id": tenant.id, "schema_name": tenant.schema_name, "domain": domain})
