from catalog.models import Product, Manufacturer, Gallery, Currency

from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField


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


class ManufacturerValueSerializer(serializers.Serializer):
    name = serializers.CharField()


class ManufacturerCountriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('manufacturer_countries',)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для подгрузки товара."""
    in_cart = SerializerMethodField()

    currency = CurrencySerializer(read_only=True)
    gallery_images = GallerySerializer(read_only=True, many=True)
    manufacturer = ManufacturerSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_in_cart(self, obj):
        request = self.context['request']
        if 'in_cart' in request.session:
            return obj.id in request.session['in_cart']
        return False
