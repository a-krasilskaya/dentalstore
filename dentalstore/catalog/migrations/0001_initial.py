# Generated by Django 4.2.4 on 2023-08-22 15:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Название категории товара')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='slug')),
                ('image', models.ImageField(upload_to='static/uploads/images/%Y/%m', verbose_name='Изображение')),
                ('alt', models.CharField(blank=True, max_length=255, verbose_name='Атрибут alt')),
                ('supplier_url', models.URLField(blank=True, verbose_name='URL')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='catalog.productcategory', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название товара')),
                ('slug', models.SlugField(max_length=155, unique=True, verbose_name='slug')),
                ('description', models.TextField(verbose_name='Описание товара')),
                ('sku', models.CharField(max_length=255, verbose_name='Артикул')),
                ('barcode', models.CharField(blank=True, max_length=255, verbose_name='Код')),
                ('manufacturer', models.CharField(blank=True, max_length=255, verbose_name='Производитель')),
                ('manufacturer_countries', models.CharField(blank=True, max_length=255, verbose_name='Страна-производитель')),
                ('unit_measure', models.CharField(blank=True, max_length=255, verbose_name='Единица измерения')),
                ('length', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Длина (мм.)')),
                ('width', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Ширина (мм.)')),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Высота (мм.)')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Вес (г.)')),
                ('price', models.DecimalField(decimal_places=2, default=1, max_digits=20, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('sale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена со скидкой')),
                ('currency', models.CharField(max_length=255, verbose_name='Валюта')),
                ('quantity', models.IntegerField(default=0, null=True, verbose_name='Количество товара')),
                ('stock', models.IntegerField(blank=True, default=0, null=True, verbose_name='Акция')),
                ('new_product', models.BooleanField(blank=True, null=True, verbose_name='Новинка')),
                ('hit_sales', models.BooleanField(blank=True, null=True, verbose_name='Хит продаж')),
                ('publish', models.BooleanField(default=True, verbose_name='Опубликовано')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('category', mptt.fields.TreeForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='catalog.productcategory', verbose_name='Категория товара')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery')),
                ('alt', models.CharField(blank=True, max_length=255, verbose_name='Атрибут alt')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.product')),
            ],
        ),
    ]
