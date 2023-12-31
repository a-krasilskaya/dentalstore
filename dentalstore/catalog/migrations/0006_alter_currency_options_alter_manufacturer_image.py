# Generated by Django 4.2.4 on 2023-08-22 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_currency_options_currency_currency_sign'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name': 'Валюта'},
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/uploads/images/%Y/%m', verbose_name='Изображение'),
        ),
    ]
