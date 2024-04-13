from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class CustomUser(AbstractUser):
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL пользователя")
    # photo = models.ImageField(verbose_name="Фото", blank=True, null=True)

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug': self.slug})
