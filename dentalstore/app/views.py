from django.conf import settings
from django.contrib import messages
from django.core.files import images
from django.shortcuts import render, redirect
import logging

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.models import Banner, Sertificate
from catalog.models import Manufacturer, Product, ProductCategory, Gallery
from feedback.forms import OrderCallBackForm, FeedBackForm
from django.http import FileResponse, HttpResponse
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
    sertificates = Sertificate.objects.all()
    return render(request, 'app/sertificate.html', {'sertificates': sertificates})


def image_to_pdf(request, image_name):
    # Полный путь к изображению
    image_path = os.path.join(settings.MEDIA_ROOT, image_name)

    # Создание HTTP ответа с типом содержимого PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="image.pdf"'

    # Создание объекта PDF
    c = canvas.Canvas(response, pagesize=letter)

    # Добавление изображения в PDF. Размеры и положение можно настроить
    c.drawImage(image_path, 0, 0, width=595, height=842, preserveAspectRatio=True)

    # Сохранение PDF
    c.showPage()
    c.save()

    return response


def list_images(request):
    # Получение списка имен файлов изображений
    images_dir = 'static/uploads/images'
    image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

    # Передача списка в шаблон
    return render(request, 'list_images.html', {'images': image_files})