# Generated by Django 4.2.4 on 2023-11-26 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_product_restriction_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='restriction_sale',
            field=models.BooleanField(default=False, verbose_name='Ограничение продажи для физ лиц'),
        ),
    ]
