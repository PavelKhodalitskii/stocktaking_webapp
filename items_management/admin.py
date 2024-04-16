from django.contrib import admin

from .models import InventoryItems
# Register your models here.

@admin.register(InventoryItems)
class InventoryItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'item_number')