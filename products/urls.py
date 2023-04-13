from django.urls import path

from products.views import products, product_to_basket, product_off_basket

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),

    path('category/<int:category_id>',
         products,
         name='category'),

    path('page/<int:page>/',
         products,
         name='paginator'),

    path('user/add/<int:product_id>',
         product_to_basket,
         name='product_to_basket'),

    path('user/remove/<int:basket_id>',
         product_off_basket,
         name='product_off_basket'),
]
