# Generated by Django 4.2.4 on 2023-08-27 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_product_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='img',
        ),
    ]
