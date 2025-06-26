from django.contrib import admin
from django.urls import path, include
from customers.views import create_customer, approve_customer, list_tenants, pending_requests, signup
from core.views import home, dashboard, service_list, service_create, task_list, task_create, all_services, all_tasks, client_list, client_create

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/create_customer/', create_customer, name='create_customer'),
    path('approve/<int:pk>/', approve_customer, name='approve_customer'),
    path('api/tenants/', list_tenants, name='list_tenants'),
    path('api/requests/', pending_requests, name='pending_requests'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('services/', service_list, name='service_list'),
    path('services/new/', service_create, name='service_create'),
    path('tasks/', task_list, name='task_list'),
    path('tasks/new/', task_create, name='task_create'),
    path('clients/', client_list, name='client_list'),
    path('clients/new/', client_create, name='client_create'),
    path('all_services/', all_services, name='all_services'),
    path('all_tasks/', all_tasks, name='all_tasks'),
    path('', home, name='home'),
]
