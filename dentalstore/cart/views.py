from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from catalog.models import Product, Gallery
from .cart import Cart
from .forms import CartAddProductForm
# from app.middlewares import AjaxMiddleware


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 update_quantity=cd['update'])
    # return redirect('cart:cart_detail')
    if is_ajax(request=request):
        print('ajax')
        return JsonResponse(data={'success': 'Товар добавлен в корзину'}, status=201)
    else:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart, 'images': Gallery.objects.all()})




