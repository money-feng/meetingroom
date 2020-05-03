from django.contrib import admin
from .models import UserProfile, Department, MenuList
# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(MenuList)
class MenuListAdmin(admin.ModelAdmin):
    pass