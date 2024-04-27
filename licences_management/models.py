from django.db import models
from django.urls import reverse

from account.models import CustomUser

# Create your models here.


class Licence(models.Model):
    class Meta:
        verbose_name = 'Лицензия'
        verbose_name_plural = 'Лицензии'

    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL лицензии")
    name = models.CharField(max_length=75, verbose_name="Имя лицензии")
    #data = models.DateTimeField()
    valid_from = models.DateTimeField(verbose_name="Действительно с")
    valid_to = models.DateTimeField(verbose_name="Действительно по")
    type = models.ForeignKey('LicenceType', related_name='licence', null=True, on_delete=models.SET_NULL)
    users = models.ManyToManyField(CustomUser, related_name='licences')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('licence', kwargs={'licence_slug': self.slug})


class LicenceType(models.Model):
    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
    name = models.CharField(max_length=75, verbose_name="Имя типа")

    def __str__(self):
        return self.name


