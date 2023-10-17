from django.contrib import admin

from .models import OrderItem, Order


# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'email', 'address',
                     'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
