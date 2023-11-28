from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin  # для древовидной структуры категорий
from catalog.models import Product, ProductCategory, Gallery, Manufacturer, Currency, TagProduct


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


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'sale_price', 'quantity', 'publish', 'created', 'updated']
    inlines = [GalleryInline, ]
    filter_horizontal = ['tags', ]
    list_filter = ['publish', 'created']
    list_editable = ['quantity', 'publish']
    prepopulated_fields = {'slug': ('title',)}



    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


admin.site.register(Product, ProductAdmin)



