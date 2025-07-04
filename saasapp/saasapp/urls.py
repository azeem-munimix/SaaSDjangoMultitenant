from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from customers.views import create_customer, approve_customer, list_tenants, pending_requests, signup
from core.views import (
    home,
    dashboard,
    service_list,
    service_create,
    task_list,
    task_create,
    all_services,
    all_tasks,
    client_list,
    client_create,
    foia_request_create,
    foia_request_list,
    foia_request_accept,
    foia_request_assign,
    resident_signup,
    logout,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout, name='logout'),
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
    path('foia/new/', foia_request_create, name='foia_create'),
    path('foia/', foia_request_list, name='foia_list'),
    path('foia/<int:pk>/accept/', foia_request_accept, name='foia_accept'),
    path('foia/<int:pk>/assign/', foia_request_assign, name='foia_assign'),
    path('resident_signup/', resident_signup, name='resident_signup'),
    path('clients/', client_list, name='client_list'),
    path('clients/new/', client_create, name='client_create'),
    path('all_services/', all_services, name='all_services'),
    path('all_tasks/', all_tasks, name='all_tasks'),
    path('', home, name='home'),
]
