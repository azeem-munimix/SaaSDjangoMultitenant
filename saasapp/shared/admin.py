from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CoreUser

@admin.register(CoreUser)
class CoreUserAdmin(UserAdmin):
    pass
