import json

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse  # для древовидной структуры категорий
from mptt.models import MPTTModel, TreeForeignKey  # для древовидной структуры категорий
from django.core.validators import MinValueValidator  # валидатор значений


from users.models import User


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(max_length=155, verbose_name='slug', null=False, unique=True)
    description = models.TextField(verbose_name='Описание товара')
    category = TreeForeignKey('ProductCategory', on_delete=models.PROTECT, default=1,
                              related_name='products', verbose_name='Категория товара')

    # meta
    sku = models.CharField(max_length=255, verbose_name='Артикул', unique=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE, related_name='products', verbose_name='Производитель')
    manufacturer_countries = models.CharField(max_length=255, verbose_name='Страна-производитель', blank=True)
    unit_measure = models.CharField(max_length=255, verbose_name='Единица измерения', blank=True)

    # габариты
    length = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Длина (мм.)', null=True, blank=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ширина (мм.)', null=True, blank=True)
    height = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Высота (мм.)', null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес (г.)', null=True, blank=True)

    # цена и остатки
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Цена', default=1,
                                validators=[MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Цена со скидкой',
                                     null=True, blank=True, validators=[MinValueValidator(0)])
    currency = models.ForeignKey('Currency', on_delete=models.PROTECT, related_name='products')
    quantity = models.IntegerField(verbose_name='Количество товара', default=0, null=True)

    # акции, хиты продаж, новинки
    stock = models.IntegerField(verbose_name='Акция', default=0, null=True, blank=True)
    new_product = models.BooleanField(verbose_name='Новинка', null=True, blank=True)
    hit_sales = models.BooleanField(verbose_name='Хит продаж', null=True, blank=True)

    # мета публикации
    publish = models.BooleanField(verbose_name='Опубликовано', default=True)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)


    # Метка ограничеие продажи товаров
    restriction_sale = models.BooleanField(verbose_name='Ограничение продажи для физ лиц', default=False)

    # Тэги
    tags = models.ManyToManyField('TagProduct', blank=True, related_name='tags')


    class Meta:
        ordering = ['pk']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})


    def __str__(self):
        return f'{self.title} --- {self.price}'


class TagProduct(models.Model):
    tag = models.CharField(max_length=255, db_index=True, verbose_name='Тэг')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='parent_tag')

    def get_absolute_url(self):

        return reverse('product_tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return f'{self.tag}'


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='slug', unique=True)
    image = models.ImageField(upload_to='static/uploads/images/%Y/%m', verbose_name='Изображение', null=True, blank=True)
    alt = models.CharField(max_length=255, verbose_name='Атрибут alt', blank=True)


    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return f'{self.name}'


class Gallery(models.Model):
    image = models.ImageField(upload_to='static/uploads/images')
    main_image = models.BooleanField(verbose_name='Выберите гланое изображение', default=False)
    alt = models.CharField(max_length=255, verbose_name='Атрибут alt', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')


class Currency(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название валюты')
    currency_sign = models.CharField(max_length=255, verbose_name='Знак валюты')

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюта'


    def __str__(self):
        return f'{self.name}'


class ProductCategory(MPTTModel):
    title = models.CharField(max_length=200, unique=True, verbose_name='Название категории товара')
    slug = models.SlugField(max_length=200, verbose_name='slug', null=False, unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
                            db_index=True, verbose_name='Родительская категория')
    image = models.ImageField(upload_to='static/uploads/images/%Y/%m', verbose_name='Изображение', null=True, blank=True)
    alt = models.CharField(max_length=255, verbose_name='Атрибут alt', blank=True)
    supplier_url = models.URLField(verbose_name='URL', blank=True)

    # Тэги
    # tags = models.ManyToManyField(TagProduct, blank=True, related_name='tags')


    # данные синхронизации

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('product-by-category', args=[str(self.slug)], kwargs={'path': self.get_path()})


    def __str__(self):
        return self.title


# class TagProductsIntermediate(models.Model):
#      tags = models.ForeignKey(TagProduct, on_delete=models.CASCADE)
#      products = models.ForeignKey(Product, on_delete=models.CASCADE)
     # category = TreeForeignKey(ProductCategory, on_delete=models.CASCADE)
