from django.contrib import admin
from .models import Tenant, Domain, CustomerRequest

admin.site.register(Tenant)
admin.site.register(Domain)
admin.site.register(CustomerRequest)
