from django.contrib import admin

from .models import Licence, LicenceType
# Register your models here.

@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'valid_from', 'valid_to', 'type')

@admin.register(LicenceType)
class LicenceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

