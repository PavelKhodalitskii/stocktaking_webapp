from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
# Create your models here.

class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL пользователя")
    office_building = models.ForeignKey('OfficeBuilding', related_name='users', null=True, on_delete=models.SET_NULL)
    # role = models.ForeignKey('Role', related_name='users', null=True, on_delete=models.SET_NULL)
    type = models.ForeignKey('items_management.ItemType', related_name='responsible_persons', null=True, on_delete=models.PROTECT)
    is_admin = models.BooleanField(default=False, verbose_name='Администатор')
    stocktalking_responsible = models.BooleanField(default=False, verbose_name='Ответсвенный за инвентаризацию')

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug': self.slug})
    
class Role(models.Model):
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    name = models.CharField(max_length=75, verbose_name="Имя роли")

    def __str__(self):
        return self.name

class Office(models.Model):
    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'

    name = models.CharField(max_length=255, verbose_name="Имя помещения")
    office_building = models.ForeignKey('OfficeBuilding', related_name="offices", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class OfficeBuilding(models.Model):
    class Meta:
        verbose_name = 'Офис'
        verbose_name_plural = 'Офисы'

    slug = models.SlugField(max_length=512, verbose_name="URL", unique=True)
    address = models.CharField(max_length=512, verbose_name="Адрес")

    def __str__(self):
        return self.address