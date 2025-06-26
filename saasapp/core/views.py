from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from customers.models import Tenant, CustomerRequest
from django_tenants.utils import tenant_context
from django.contrib.auth import logout

from .models import Service, Task, Customer, Client, FoiaRequest, Membership
from .forms import (
    ServiceForm,
    TaskForm,
    ClientForm,
    FoiaRequestForm,
    FoiaAssignForm,
    ResidentSignupForm,
)


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


def is_admin(user, tenant):
    return Membership.objects.filter(user=user, tenant=tenant, role=Membership.ADMIN).exists()


def is_resident(user, tenant):
    return Membership.objects.filter(user=user, tenant=tenant, role=Membership.RESIDENT).exists()


def logout(request):
    logout(request)


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
    tasks = Task.objects.select_related("service")
    if getattr(request, "tenant", None) and request.tenant.schema_name == "public":
        tasks = tasks.filter(user=request.user)
    else:
        tasks = tasks.all()
    return render(request, "task_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form})


@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, "client_list.html", {"clients": clients})


@login_required
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client_list")
    else:
        form = ClientForm()
    return render(request, "client_form.html", {"form": form})


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


@login_required
def foia_request_create(request):
    tenant = getattr(request, "tenant", None)
    if not tenant or not is_resident(request.user, tenant):
        return HttpResponseForbidden("Residents only")
    if request.method == "POST":
        form = FoiaRequestForm(request.POST)
        if form.is_valid():
            foia = form.save(commit=False)
            foia.resident = request.user
            foia.save()
            return redirect("foia_list")
    else:
        form = FoiaRequestForm()
    return render(request, "foia_request_form.html", {"form": form})


@login_required
def foia_request_list(request):
    tenant = getattr(request, "tenant", None)
    if not tenant or not is_admin(request.user, tenant):
        return HttpResponseForbidden("Admins only")
    foias = FoiaRequest.objects.select_related("resident", "assigned_to")
    return render(request, "foia_request_list.html", {"foias": foias})


@login_required
def foia_request_accept(request, pk):
    tenant = getattr(request, "tenant", None)
    if not tenant or not is_admin(request.user, tenant):
        return HttpResponseForbidden("Admins only")
    try:
        foia = FoiaRequest.objects.get(pk=pk)
    except FoiaRequest.DoesNotExist:
        return HttpResponseBadRequest("invalid request")
    foia.accepted = True
    foia.save()
    return redirect("foia_list")


@login_required
def foia_request_assign(request, pk):
    tenant = getattr(request, "tenant", None)
    if not tenant or not is_admin(request.user, tenant):
        return HttpResponseForbidden("Admins only")
    try:
        foia = FoiaRequest.objects.get(pk=pk)
    except FoiaRequest.DoesNotExist:
        return HttpResponseBadRequest("invalid request")
    if request.method == "POST":
        form = FoiaAssignForm(request.POST, tenant=tenant)
        if form.is_valid():
            member = form.cleaned_data["assignee"]
            foia.assigned_to = member.user
            foia.save()
            service, _ = Service.objects.get_or_create(name="FOIA")
            Task.objects.create(
                name=f"FOIA {foia.pk}", service=service, user=member.user
            )
            return redirect("foia_list")
    else:
        form = FoiaAssignForm(tenant=tenant)
    return render(
        request,
        "foia_assign_form.html",
        {"form": form, "foia": foia},
    )


def resident_signup(request):
    """Allow a new user to sign up as a resident on the current tenant."""
    tenant = getattr(request, "tenant", None)
    if not tenant or tenant.schema_name == "public":
        return HttpResponseForbidden("Resident signup only allowed on tenant site")
    if request.method == "POST":
        form = ResidentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Membership.objects.create(user=user, tenant=tenant, role=Membership.RESIDENT)
            login(request, user)
            return redirect("home")
    else:
        form = ResidentSignupForm()
    return render(request, "registration/resident_signup.html", {"form": form})
