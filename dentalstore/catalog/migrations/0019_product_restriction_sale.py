# Generated by Django 4.2.4 on 2023-11-09 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_manufacturer_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='restriction_sale',
            field=models.BooleanField(default=False, verbose_name='Опубликовано'),
        ),
    ]