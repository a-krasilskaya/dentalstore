# Generated by Django 4.2.4 on 2023-11-26 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_alter_product_restriction_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.AddField(
            model_name='productcategory',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='catalog.tagproduct'),
        ),
    ]
