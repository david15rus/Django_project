from django.urls import path

from products.views import ProductsView, product_to_basket, product_off_basket

app_name = 'products'

urlpatterns = [
    path('', ProductsView.as_view(), name='index'),

    path('category/<int:category_id>',
         ProductsView.as_view(),
         name='category'),

    path('page/<int:page>/',
         ProductsView.as_view(),
         name='paginator'),

    path('user/add/<int:product_id>',
         product_to_basket,
         name='product_to_basket'),

    path('user/remove/<int:basket_id>',
         product_off_basket,
         name='product_off_basket'),
]
