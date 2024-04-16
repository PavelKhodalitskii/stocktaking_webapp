from django.contrib import admin

from .models import CustomUser
# Register your models here.

@admin.register(CustomUser)
class CustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'slug')
