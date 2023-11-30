from django.core.mail import EmailMultiAlternatives

from cart.cart import Cart
from django.shortcuts import render

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
            # clear the cart
            cart.clear()
            msg = EmailMultiAlternatives(subject='Новая заявка "Пользователь написал сообщение"',
                                         to=['store.onine1@gmail.com'])
            msg.attach_alternative(html_body, 'text/html')
            msg.send()
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})
