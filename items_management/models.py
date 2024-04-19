from django.db import models
from django.urls import reverse
from django.utils import timezone

from account.models import CustomUser, Office

# Create your models here.

class InventoryItems(models.Model):
    class Meta:
        verbose_name = 'Элемент инвентаря'
        verbose_name_plural = 'Элементы инвентаря'

    item_number = models.CharField(max_length=75, verbose_name="Инвентарный номер")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    name = models.CharField(max_length=255, verbose_name="Имя")
    value = models.FloatField(default=0.00, verbose_name="Стоимость")
    amount = models.IntegerField(null=False)
    assessed_value = models.FloatField(default=0.00, verbose_name="Оценочная стоимость")
    status = models.ForeignKey('Status', related_name="inventory_items", null=True, blank=True, on_delete=models.SET_NULL)
    office = models.ForeignKey(Office, related_name="inventory_items", null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey('ItemType', related_name="inventory_items", null=True, blank=True, on_delete=models.SET_NULL)
    financially_responsible_person = models.ForeignKey(CustomUser, related_name="related_items", blank=True, null=True, on_delete=models.CASCADE)
    valid_from = models.DateTimeField(verbose_name="Действительно с", default=timezone.now)

    def __str__(self):
        return str(self.name) + str(self.item_number)
    
    def get_absolute_url(self):
        return reverse('inventory_item', kwargs={'item_slug': self.slug})
    
class ItemType(models.Model):
    class Meta:
        verbose_name = 'Тип предметов инвентаря'
        verbose_name_plural = 'Типы предметов инвентаря'

    name = models.CharField(max_length=75, verbose_name='Имя типа')

class Status(models.Model):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    name = models.CharField(max_length=75, verbose_name='Имя статуса')