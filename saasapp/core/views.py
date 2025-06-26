from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from customers.models import Tenant, CustomerRequest
from django_tenants.utils import tenant_context

from .models import Service, Task, Customer
from .forms import ServiceForm, TaskForm


@login_required
def home(request):
    tenant = getattr(request, "tenant", None)
    customer = None
    if tenant:
        try:
            customer = Customer.objects.select_related("owner").get()
        except Customer.DoesNotExist:
            customer = None
    return render(request, "home.html", {"tenant": tenant, "customer": customer})


def is_core(user):
    return getattr(user, "is_core", False) or user.is_superuser


@user_passes_test(is_core)
def dashboard(request):
    tenants = Tenant.objects.all()
    requests = CustomerRequest.objects.filter(approved=False)
    return render(request, "dashboard.html", {"tenants": tenants, "requests": requests})


@login_required
def service_list(request):
    services = Service.objects.all()
    return render(request, "service_list.html", {"services": services})


@login_required
def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("service_list")
    else:
        form = ServiceForm()
    return render(request, "service_form.html", {"form": form})


@login_required
def task_list(request):
    tasks = Task.objects.select_related("service").all()
    return render(request, "task_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form})


@user_passes_test(is_core)
def all_services(request):
    records = []
    for tenant in Tenant.objects.all():
        with tenant_context(tenant):
            for service in Service.objects.all():
                records.append({"tenant": tenant, "service": service})
    return render(request, "all_services.html", {"records": records})


@user_passes_test(is_core)
def all_tasks(request):
    records = []
    for tenant in Tenant.objects.all():
        with tenant_context(tenant):
            for task in Task.objects.select_related("service").all():
                records.append({"tenant": tenant, "task": task})
    return render(request, "all_tasks.html", {"records": records})
