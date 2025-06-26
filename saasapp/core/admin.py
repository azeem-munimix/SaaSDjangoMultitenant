from django.contrib import admin
from .models import Item, Service, Task, Customer, Membership, FoiaRequest

admin.site.register(Item)
admin.site.register(Service)
admin.site.register(Task)
admin.site.register(Customer)
admin.site.register(Membership)
admin.site.register(FoiaRequest)
