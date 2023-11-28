from django import forms

from catalog.models import Product, Manufacturer

# Manufacturer_Countries = Product.objects.all()
# availability = ['В наличии', 'Под заказ']

class ProductsFilterForm(forms.Form):
    min_price = forms.IntegerField(label='от', required=False)
    max_price = forms.IntegerField(label='до', required=False)
    manufacturer = forms.ModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(),
        label="Производитель",
        widget=forms.CheckboxSelectMultiple)
    countries = forms.ModelMultipleChoiceField(
        queryset=Product.objects.values_list('manufacturer_countries', flat=True).distinct(),
        # queryset=Product.objects.order_by("manufacturer_countries").distinct("manufacturer_countries"),
        # queryset=Product.objects.values('manufacturer_countries').distinct("manufacturer_countries"),
        label="Страна",
        widget=forms.CheckboxSelectMultiple)
    # availability = forms.MultipleChoiceField(
    #                     choices=availability,
    #                     label="Наличие товара",
    #                     widget=forms.CheckboxSelectMultiple())


