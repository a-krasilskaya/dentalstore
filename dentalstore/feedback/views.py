from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import OrderCallBackForm, FeedBackForm
from django.template.loader import render_to_string
from django.views.generic import View
from django.http import JsonResponse


# class OrderCallBackFormView(View):
#     def post(self, request):
#         form = OrderCallBackForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, settings.MY_INFO,
#                              "Спасибо за заявку, наш сотрудник позвонит вам в ближайшее время")
#             name = form.cleaned_data['name']
#             phone = form.cleaned_data['phone']
#         #     print(request.POST.get('url_form'))
#             html_body = render_to_string('app/application_main_page.html', {'name': name, 'phone': phone})
#
#             msg = EmailMultiAlternatives(subject='Новая заявка "Заказать звонок"', to=['store.onine1@gmail.com'])
#             msg.attach_alternative(html_body, 'text/html')
#             msg.send()
#         else:
#             messages.add_message(request, settings.MY_INFO, "Заполните обязательные поля")
#         return redirect("/")


class OrderCallBackFormView(View):
    def post(self, request):
        form = OrderCallBackForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone']
            }
            form.save()
            html_body = render_to_string('app/application_main_page.html', data)

            msg = EmailMultiAlternatives(subject='Новая заявка "Заказать звонок"', to=['store.onine1@gmail.com'])
            msg.attach_alternative(html_body, 'text/html')
            msg.send()
            return JsonResponse(data={'success': "Спасибо за заявку, наш сотрудник позвонит вам в ближайшее время"}, status=201)
        else:
            return JsonResponse(data={'error': "Заполните обязательные поля"}, status=400)


# class FeedBackFormView(View):
#     def post(self, request):
#         form = FeedBackForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, settings.MY_INFO,
#                              "Спасибо за заявку, наш сотрудник позвонит вам в ближайшее время")
#             name = form.cleaned_data['name']
#             phone = form.cleaned_data['phone']
#             email = form.cleaned_data['email']
#             text_message = form.cleaned_data['text_message']
#         #     print(request.POST.get('url_form'))
#             html_body = render_to_string('app/application_contacts_page.html', {'name': name, 'phone': phone, 'email': email, 'text_message': text_message})
#
#             msg = EmailMultiAlternatives(subject='Новая заявка "Пользователь написал сообщение"', to=['store.onine1@gmail.com'])
#             msg.attach_alternative(html_body, 'text/html')
#             msg.send()
#         else:
#             messages.add_message(request, settings.MY_INFO, "Заполните обязательные поля")
#         return redirect("/contacts")

class FeedBackFormView(View):
    def post(self, request):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            data = {
                'name': form.cleaned_data['name'],
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'text_message': form.cleaned_data['text_message']
            }
            form.save()
            html_body = render_to_string('app/application_contacts_page.html', data)

            msg = EmailMultiAlternatives(subject='Новая заявка "Пользователь написал сообщение"', to=['store.onine1@gmail.com'])
            msg.attach_alternative(html_body, 'text/html')
            msg.send()
            return JsonResponse(data={'success': "Спасибо за заявку, наш сотрудник позвонит вам в ближайшее время"}, status=201)
        else:
            return JsonResponse(data={'error': "Заполните обязательные поля"}, status=400)
