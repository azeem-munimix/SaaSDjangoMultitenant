from django.contrib import admin
from django.urls import path, include
from customers.views import create_customer, approve_customer, list_tenants, pending_requests, signup
from core.views import home, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/create_customer/', create_customer, name='create_customer'),
    path('approve/<int:pk>/', approve_customer, name='approve_customer'),
    path('api/tenants/', list_tenants, name='list_tenants'),
    path('api/requests/', pending_requests, name='pending_requests'),
    path('signup/', signup, name='signup'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', home, name='home'),
]
