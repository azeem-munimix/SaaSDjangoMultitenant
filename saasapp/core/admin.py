from django.contrib import admin
from .models import Item, Service, Task, Customer

admin.site.register(Item)
admin.site.register(Service)
admin.site.register(Task)
admin.site.register(Customer)
