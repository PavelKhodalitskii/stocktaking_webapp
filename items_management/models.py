from django.db import models
from django.urls import reverse
from django.utils import timezone

from account.models import CustomUser, Office
from .utils import generate_qr_code

# Create your models here.

class InventoryItems(models.Model):
    class Meta:
        verbose_name = 'Элемент инвентаря'
        verbose_name_plural = 'Элементы инвентаря'

    #Общая информация
    item_number = models.CharField(max_length=75, verbose_name="Инвентарный номер")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    name = models.CharField(max_length=255, verbose_name="Имя")
    office = models.ForeignKey(Office, related_name="inventory_items", verbose_name="Помещение", null=True, blank=True, on_delete=models.SET_NULL)
    type = models.ForeignKey('ItemType', related_name="inventory_items", verbose_name="Тип", null=True, blank=True, on_delete=models.SET_NULL)
    financially_responsible_person = models.ForeignKey(CustomUser, related_name="related_items", verbose_name="Финансово ответсвенное лицо", blank=True, null=True, on_delete=models.CASCADE)
    
    #Данные бухгалтеского учета
    value = models.FloatField(default=0.00, verbose_name="Стоимость")
    amount = models.IntegerField(null=False, default=0, verbose_name="Количество")

    #Фактическое состояние
    assessed_value = models.FloatField(default=0.00, verbose_name="Оценочная стоимость")
    assessed_amount = models.IntegerField(null=False, default=0, verbose_name="Оценочное количество")
    status = models.ForeignKey('Status', related_name="inventory_items", verbose_name="Статус", null=True, blank=True, on_delete=models.SET_NULL)
    valid_from = models.DateTimeField(verbose_name="Действительно с", default=timezone.now)
    qr_file_path = models.CharField(default="", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.qr_file_path = generate_qr_code(self)

    def get_qr_code(self):
        return self.qr_file_path

    def __str__(self):
        return str(self.name) + str(self.item_number)
    
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'item_slug': self.slug, 'officebuilding_slug': self.office.office_building.slug})
    
class ItemType(models.Model):
    class Meta:
        verbose_name = 'Тип предметов инвентаря'
        verbose_name_plural = 'Типы предметов инвентаря'

    name = models.CharField(max_length=75, verbose_name='Имя типа')

    def __str__(self):
        return self.name

class Status(models.Model):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    name = models.CharField(max_length=75, verbose_name='Имя статуса')

    def __str__(self):
        return self.name