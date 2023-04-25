from django.urls import path

from orders.views import OrderCreateView, OrderSuccessView, OrderListView

app_name = 'orders'

urlpatterns = [
    path('create', OrderCreateView.as_view(), name='order_create'),
    path('success/', OrderSuccessView.as_view(), name='success'),
    path('', OrderListView.as_view(), name='orders_list'),

]
