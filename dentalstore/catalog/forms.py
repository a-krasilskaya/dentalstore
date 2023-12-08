from django import forms

from catalog.models import Product, Manufacturer


# ManufacturerCountries = Product.objects.all()
# availability = ['В наличии', 'Под заказ']


class ProductsFilterForm(forms.Form):
    min_price = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={'placeholder': 'от', 'class': 'form-control'}))
    max_price = forms.IntegerField(label='', required=False, widget=forms.NumberInput(attrs={'placeholder': 'до', 'class': 'form-control'}))
    ordering = forms.ChoiceField(label='Сортировать по', required=False, widget=forms.Select(attrs={'class': 'form-control'}), choices=[
        ['title', 'Алфавиту'],
        ['price', 'Цене min'],
        ['-price', 'Цене max'],
    ])
    manufacturer = forms.ModelMultipleChoiceField(
        queryset=Product.objects.values_list('manufacturer__name', flat=True).order_by('manufacturer__name').distinct('manufacturer__name'),
        label="Производитель",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form_filter_checkbox'}))
    countries = forms.ModelMultipleChoiceField(
        queryset=Product.objects.values_list('manufacturer_countries', flat=True).order_by('manufacturer_countries').distinct('manufacturer_countries'),
        label="Страна",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form_filter_checkbox'}))
    # availability = forms.MultipleChoiceField(
    #                     choices=availability,
    #                     label="Наличие товара",
    #                     widget=forms.CheckboxSelectMultiple())


