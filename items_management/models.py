from django.db import models
from django.urls import reverse

from account.models import CustomUser

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
    # status = models.ForeignKey()
    financially_responsible_person = models.ForeignKey(CustomUser, related_name="related_items", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + str(self.item_number)
    
    def get_absolute_url(self):
        return reverse('inventory_item', kwargs={'item_slug': self.slug})