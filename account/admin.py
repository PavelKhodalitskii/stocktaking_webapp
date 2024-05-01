from django.contrib import admin

from .models import CustomUser, Office, OfficeBuilding, Role
# Register your models here.

@admin.register(CustomUser)
class CustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'slug')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'office_building')

@admin.register(OfficeBuilding)
class OfficeBuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'address')