from django.contrib import admin

from .models import InventoryItems, ItemType, Status
# Register your models here.

@admin.register(InventoryItems)
class InventoryItemsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'item_number')

@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')