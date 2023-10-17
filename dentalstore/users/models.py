from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    clinic_name = models.CharField(verbose_name='Название клиники', max_length=255, blank=True, null=True)
    clinic_address = models.CharField(verbose_name='Адрес клиники', max_length=255, blank=True, null=True)
    clinic_phone = models.CharField(verbose_name='Телефон клиники', max_length=255, blank=True, null=True)
    clinic_email = models.EmailField(verbose_name='Email клиники', max_length=255, blank=True, null=True)
    clinic_site = models.CharField(verbose_name='Сайт клиники', max_length=255, blank=True, null=True)
