from django.db import models

# Create your models here.


class Licence(models.Model):
    class Meta:
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'
    name = models.CharField(max_length=75, verbose_name="Имя лицензии")
    #data = models.DateTimeField()
    valid_from = models.DateTimeField(verbose_name="Действительно с")
    valid_to = models.DateTimeField(verbose_name="Действительно по")
    type = models.ForeignKey('LicenceType', related_name='licences', null=True, on_delete=models.SET_NULL)


class LicenceType(models.Model):
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
    name = models.CharField(max_length=75, verbose_name="Имя типа")


