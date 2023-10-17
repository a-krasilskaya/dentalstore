from django import forms

from .models import CallOrderForm, SendMessageForm


class OrderCallBackForm(forms.ModelForm):
    class Meta:
        model = CallOrderForm
        fields = ['name', 'phone', 'consent']
        labels = {
            'name': '',
            'phone': '',
            'consent': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'form-control'}),
        }
        help_texts = {
            'consent': (f'Я даю согласие на обработку своих персональных данных.'),
        }



class FeedBackForm(forms.ModelForm):
    class Meta:
        model = SendMessageForm
        fields = ['name', 'phone', 'email', 'text_message', 'consent']
        labels = {
            'name': '',
            'phone': '',
            'email': '',
            'text_message': '',
            'consent': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
            'text_message': forms.Textarea(attrs={'placeholder': 'Введите ваше сообщение', 'class': 'form-control', 'rows': '5'}),
        }
        help_texts = {
            'consent': (f'Я даю согласие на обработку своих персональных данных.'),
        }