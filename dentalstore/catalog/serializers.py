from catalog.models import Product, Manufacturer, Gallery, Currency
from rest_framework import serializers


class GallerySerializer(serializers.ModelSerializer):
    """Сериализатор для подгрузки изображений."""

    class Meta:
        model = Gallery
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    """Сериализатор для подгрузки валюты."""

    class Meta:
        model = Currency
        fields = "__all__"


class ManufacturerSerializer(serializers.ModelSerializer):
    """Сериализатор для подгрузки производителей товара."""

    class Meta:
        model = Manufacturer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для подгрузки товара."""
    currency = CurrencySerializer(read_only=True)
    gallery_images = GallerySerializer(read_only=True, many=True)
    manufacturer = ManufacturerSerializer(read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
        # fields = ['title', 'manufacturer', 'manufacturer_countries', 'price', 'sale_price', 'availability', 'sku', 'currency_sign', 'quantity', 'gallery_images']