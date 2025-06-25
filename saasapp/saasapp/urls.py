from django.contrib import admin
from django.urls import path
from customers.views import create_customer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create_customer/', create_customer, name='create_customer'),
]
