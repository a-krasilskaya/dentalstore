from django.contrib import admin

from .models import Banner
from django.utils.safestring import mark_safe


class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "text", "image", "image_show"]
    readonly_fields = ["image_show"]

    def image_show(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="60" />'.format(obj.image.url))
        return 'None'

    image_show.__name__ = 'Изображение'


admin.site.register(Banner, BannerAdmin)

