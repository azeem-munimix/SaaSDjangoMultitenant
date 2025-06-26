import json
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django_tenants.utils import schema_context
from .models import Tenant, Domain, CustomerRequest
from .forms import CustomerSignupForm


def is_core(user):
    return getattr(user, "is_core", False) or user.is_superuser


@user_passes_test(is_core)
def approve_customer(request, pk):
    try:
        req = CustomerRequest.objects.get(pk=pk, approved=False)
    except CustomerRequest.DoesNotExist:
        return HttpResponseBadRequest("invalid request")

    with schema_context('public'):
        tenant = Tenant(schema_name=req.schema_name, name=req.name)
        tenant.save()
        Domain.objects.create(domain=req.domain, tenant=tenant, is_primary=True)
    req.approved = True
    req.save()
    return JsonResponse({"status": "approved", "tenant": tenant.schema_name})

@csrf_exempt
@login_required
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

    CustomerRequest.objects.create(
        user=request.user,
        name=name,
        domain=domain,
        schema_name=schema_name,
    )

    return JsonResponse({"status": "pending"})


@user_passes_test(is_core)
def list_tenants(request):
    tenants = Tenant.objects.all().select_related(None)
    data = [
        {"id": t.id, "schema_name": t.schema_name, "name": t.name} for t in tenants
    ]
    return JsonResponse({"tenants": data})


@user_passes_test(is_core)
def pending_requests(request):
    reqs = CustomerRequest.objects.filter(approved=False)
    data = [
        {"id": r.id, "name": r.name, "domain": r.domain, "schema_name": r.schema_name, "user": r.user.username}
        for r in reqs
    ]
    return JsonResponse({"requests": data})


def signup(request):
    """Allow a new user to sign up and request a customer tenant."""
    if request.method == "POST":
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data["name"]
            domain = form.cleaned_data["domain"]
            schema_name = (
                form.cleaned_data.get("schema_name")
                or name.lower().replace(" ", "_")
            )
            CustomerRequest.objects.create(
                user=user,
                name=name,
                domain=domain,
                schema_name=schema_name,
            )
            login(request, user)
            return redirect("home")
    else:
        form = CustomerSignupForm()

    return render(request, "registration/signup.html", {"form": form})
