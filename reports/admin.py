from django.contrib import admin

from .models import StocktalkingReport, Invents, RelationItemsReports
# Register your models here.

@admin.register(StocktalkingReport)
class StocktalkingReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'type', 'invent')

@admin.register(Invents)
class InventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'data_start', 'data_end', 'responsible_person', 'office_building')

@admin.register(RelationItemsReports)
class RelationItemsReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'report', 'datatime', 'assessed_value', 'status')
