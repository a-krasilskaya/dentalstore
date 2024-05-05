from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
import logging

from app.models import Banner
from catalog.models import Manufacturer, Product, ProductCategory, Gallery
from feedback.forms import OrderCallBackForm, FeedBackForm
from django.http import FileResponse
import os

logger = logging.getLogger(__name__)


def home(request):
    context = {
        'title': 'TemplateProject',
        'banners': Banner.objects.filter(publish=True),
        'manufacturer': Manufacturer.objects.all(),
        'category': ProductCategory.objects.filter(parent=True),
        'bestsellers': Product.objects.filter(hit_sales=True),
        'form': OrderCallBackForm(),
        'product_images': Gallery.objects.all()
    }

    # if request.method == 'POST':
    #     form = ContactForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         print("Отправлено")
    #         messages.add_message(request, settings.MY_INFO,
    #                              "Спасибо за заявку, наш сотрудник позвонит вам в ближайшее время")
    # else:
    #     messages.add_message(request, settings.MY_INFO,
    #                          "не отправлено")
    #     context['form'] = ContactForm()

    return render(request, 'app/main.html', context)


def delivery(request):
    return render(request, 'app/delivery.html')


def contacts(request):
    return render(request, 'app/contacts.html', {'form': FeedBackForm()})


def privacy_policy(request):
    return render(request, 'app/privacy_policy.html')


def about(request):
    return render(request, 'app/about.html')


def sertificate(request):
    return render(request, 'app/sertificate.html')
