from typing import Any, Iterable
from django.db import models
from django.urls import reverse

# Create your models here.
from items_management.models import InventoryItems, ItemType, Status
from account.models import CustomUser, OfficeBuilding

class StocktalkingReport(models.Model):
    class Meta:
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёт'
    
    author = models.ForeignKey(CustomUser, related_name='report', null=True, on_delete=models.SET_NULL, verbose_name="Автор")
    ivent = models.ForeignKey('Ivent', related_name='report', null=True, on_delete=models.SET_NULL, verbose_name="Ивент инвенатризации")
    type = models.ForeignKey(ItemType, related_name='report', null=True, on_delete=models.SET_NULL, verbose_name="Тип")
    items = models.ManyToManyField(InventoryItems, through='RelationItemsReports', related_name='reports', verbose_name="Предметы")
    note = models.CharField(max_length=255, blank=True, verbose_name="Примечание")
    finish_datetime = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Отчёт инвентаризации " + str(self.pk)
    
    def get_absolute_url(self):
        return reverse('stocktalking_report', kwargs={'report_slug': self.slug})


class Ivent(models.Model):
    class Meta:
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризации'

    data_start = models.DateTimeField(verbose_name="Дата начала")
    data_end = models.DateTimeField(verbose_name="Дата окончания")
    responsible_person = models.ForeignKey(CustomUser, related_name='invents', null=True, on_delete=models.SET_NULL, verbose_name="Ответсвенное лицо")
    office_building = models.ForeignKey(OfficeBuilding, related_name='invents', null=True, on_delete=models.SET_NULL, verbose_name="Здание офиса")

    def save(self, *args, **kwargs):
        is_created = self.pk is None

        super(Ivent, self).save(*args, **kwargs)

        if is_created:
            item_types = ItemType.objects.all()
            for item_type in item_types:
                report = StocktalkingReport(ivent=self, type=item_type)
                report.save()
                items_related = InventoryItems.objects.all().filter(office__office_building = self.office_building).filter(type=item_type)
                for item in items_related:
                    relation = RelationItemsReports(item=item, report=report)
                    relation.save()

    def __str__(self):
        return "Инвентаризация " + str(self.office_building) + "; " + f"{str(self.data_start)} - {str(self.data_end)}"
    # Написать метод save()


#Написать сериализаторы
class RelationItemsReports(models.Model):
    class Meta:
        verbose_name = 'Отношение: Предметы-Отчёты'
        verbose_name_plural = 'Отношения: Предметы-Отчёты'

    item = models.ForeignKey(InventoryItems, null=True, on_delete=models.SET_NULL, verbose_name="Предмет")
    report = models.ForeignKey(StocktalkingReport, null=True, on_delete=models.SET_NULL, verbose_name="Отчет")
    last_scan_datetime = models.DateTimeField(null=True, blank=True)
    assessed_value = models.FloatField(default=0.00, verbose_name="Оценочная стоимость")
    assessed_amount = models.IntegerField(default=0, verbose_name="Оценочное кол-во")
    status = models.ForeignKey(Status, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Статус")
    note = models.TextField(null=True, blank=True, verbose_name="Примечание")
    approve = models.BooleanField(default=False, verbose_name="Подтверждено")
