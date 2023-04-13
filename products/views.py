from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

from products.models import Category, Products, Basket


class IndexView(TemplateView):
    title = 'Store - Главная'


def index(request):
    context = {
        'title': 'Test title',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    if category_id:
        products = Products.objects.filter(category=category_id)
    else:
        products = Products.objects.all()

    per_page = 3
    paginator = Paginator(products, 3)
    products_paginator = paginator.page(page)

    context = {
        'title': 'Store - Магазин',
        'products': products_paginator,
        'categories': Category.objects.all(),
    }
    return render(request, 'products/products.html', context)


@login_required
def product_to_basket(request, product_id):
    product = Products.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        user_basket = basket.first()
        user_basket.quantity += 1
        user_basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def product_off_basket(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
