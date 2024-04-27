from django.db import models
from django.urls import reverse

# Create your models here.
from items_management.models import InventoryItems, ItemType, Status
from account.models import CustomUser, OfficeBuilding


class StocktalkingReport(models.Model):
    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёт'
        

    author = models.ForeignKey(InventoryItems, related_name='report', null=True, on_delete=models.SET_NULL)
    invent = models.ForeignKey(ItemType, related_name='report', null=True, on_delete=models.SET_NULL)
    type = models.ForeignKey('Invents', related_name='report', null=True, on_delete=models.SET_NULL)
    items = models.ManyToManyField(InventoryItems, through='RelationItemsReports', related_name='reports')
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL лицензии")
    note = models.CharField(max_length=255, verbose_name="Примечание")

    def __str__(self):
        return "Отчёт инвентаризации " + str(self.pk)
    
    def get_absolute_url(self):
        return reverse('stocktalking_report', kwargs={'report_slug': self.slug})


class Invents(models.Model):
    class Meta:
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризации'
    data_start = models.DateTimeField()
    data_end = models.DateTimeField()
    responsible_person = models.ForeignKey(CustomUser, related_name='invents', null=True, on_delete=models.SET_NULL)
    office_building = models.ForeignKey(OfficeBuilding, related_name='invents', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Инвентаризация " + str(self.pk)


class RelationItemsReports(models.Model):
    item = models.ForeignKey(InventoryItems, null=True, on_delete=models.SET_NULL)
    report = models.ForeignKey(StocktalkingReport, null=True, on_delete=models.SET_NULL)
    datatime = models.DateTimeField()
    assessed_value = models.FloatField(default=0.00, verbose_name="Оценочная стоимость")
    status = models.ForeignKey(Status, null=True, on_delete=models.SET_NULL)

