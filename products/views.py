from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.view import TitleCommonMixin
from products.models import Basket, Category, Products


class IndexView(TitleCommonMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store - Главная'


class ProductsView(TitleCommonMixin, ListView):
    model = Products
    template_name = 'products/products.html'
    paginate_by = 3
    context_object_name = 'products'
    title = 'Store - Каталог'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsView, self).get_context_data()
        context['category_id'] = self.kwargs.get('category_id')
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = super(ProductsView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category_id=category_id)
        else:
            return queryset


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
