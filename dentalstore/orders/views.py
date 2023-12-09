from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from cart.cart import Cart
from django.shortcuts import render, redirect

from .forms import OrderCreateForm
from .models import OrderItem


# Create your views here.


def order_create(request, html_body=None):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # order send email manager
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            # print(request.POST.get('url_form'))
            html_body = render_to_string('orders/new_order.html', {'first_name': first_name,
                                                                   'last_name': last_name,
                                                                   'phone': phone,
                                                                   'email': email,
                                                                   'address': address,
                                                                   'order': order,
                                                                   'cart': cart})
            msg = EmailMultiAlternatives(subject='Новый заказ', to=['store.onine1@gmail.com'])
            msg.attach_alternative(html_body, 'text/html')
            msg.send()
            # clear the cart
            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


