from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address', 'consent']
        labels = {
            'first_name': '',
            'last_name': '',
            'phone': '',
            'email': '',
            'address': '',
            'consent': '',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Адрес доставки', 'class': 'form-control'}),
        }
        help_texts = {
            'consent': (f'Я даю согласие на обработку своих персональных данных.'),
        }