from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from customers.models import Tenant, Domain, CustomerRequest

@login_required
def home(request):
    tenant = getattr(request, "tenant", None)
    return render(request, "home.html", {"tenant": tenant})


def is_core(user):
    return getattr(user, "is_core", False) or user.is_superuser


@user_passes_test(is_core)
def dashboard(request):
    tenants = Tenant.objects.all()
    requests = CustomerRequest.objects.filter(approved=False)
    return render(request, "dashboard.html", {"tenants": tenants, "requests": requests})
