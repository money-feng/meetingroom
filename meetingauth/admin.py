from django.contrib import admin
from .models import UserProfile, Department, Permission, Roles
# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    pass