# Generated by Django 4.2.4 on 2023-09-02 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_banner_alt'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='first_image',
            field=models.BooleanField(default=True, verbose_name='Установить как первое изображение слайда'),
        ),
    ]
