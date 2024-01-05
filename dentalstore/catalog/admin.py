from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin  # для древовидной структуры категорий
from catalog.models import Product, ProductCategory, Gallery, Manufacturer, Currency, TagProduct
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# Register your models here.
# admin.site.register(Product)

class SupplierAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImagesAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class TagProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("tag", )}

admin.site.register(TagProduct, TagProductAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}

admin.site.register(Manufacturer, ManufacturerAdmin)

admin.site.register(Currency)


class ProductCategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('title',), }
    # filter_horizontal = ['tags', ]


class GalleryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    readonly_fields = ["image_show"]


    def image_show(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="60" />'.format(obj.image.url))
        return 'None'

    image_show.__name__ = 'Изображение'


admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    form = ProductsAdminForm
    list_display = ['title', 'category', 'price', 'sale_price', 'quantity', 'publish', 'created', 'updated']
    inlines = [GalleryInline, ]
    filter_horizontal = ['tags', ]
    search_fields = ('title', 'category__title', 'price', 'sale_price',)
    list_filter = ['category', 'publish', 'created']
    list_editable = ['quantity', 'publish']
    prepopulated_fields = {'slug': ('title',)}



    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


admin.site.register(Product, ProductAdmin)



