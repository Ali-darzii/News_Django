from django.urls import path
from . import views

urlpatterns = [
    path('add-product-to-order/', views.add_product_to_order, name='add_product_to_order'),
    path('change-product-order-count/', views.change_order_detail_count, name='change_product_order_count'),
    path('remove-product-order/', views.remove_order_detail, name='remove_product_order'),
    path('', views.order_basket_view, name='order_basket_view'),
    path('change-product-order-count/basket-page/', views.change_order_detail_count_in_basket_page,name='change_product_order_count_in_basket_page'),
    path('remove-product-order/basket-page/', views.remove_order_detail_in_basket_page,name='remove_product_order_in_basket_page'),

]
