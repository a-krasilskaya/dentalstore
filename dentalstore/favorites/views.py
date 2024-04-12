from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from catalog.models import Product, Gallery
from .favorites import Favorites
# from .forms import CartAddProductForm


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def favorites_toggle(request, product_id):
    favorites = Favorites(request)
    product = get_object_or_404(Product, id=product_id)
    if product_id in favorites.products:
        favorites.remove(product=product)
        title = 'Не в избранном'
    else:
        favorites.add(product=product)
        title = 'В избранном'
    if is_ajax(request=request):
        return JsonResponse(data={'success': title, 'count': len(favorites.products)}, status=201)
    else:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


def favorites_detail(request):
    favorites = Favorites(request)
    if is_ajax(request=request):
        return JsonResponse(data={'success': 'favorites/detail.html'}, status=201)
    else:
        return render(request, 'favorites/detail.html', {'favorites': favorites, 'images': Gallery.objects.all()})
