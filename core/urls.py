# All the urls that our website will require

from django.urls import path
from .views import shop_V, Home_V,my_account, checkout,search, OrderSummary_V,filter_V, product_details_V, remove_single_item_from_cart, contact_us, add_to_cart, remove_from_cart

app_name = 'core'

urlpatterns = [
    path('', Home_V.as_view(), name='home'),
    path('index', Home_V.as_view(), name='home'),
    path('shop', shop_V.as_view(), name='shop'),
    path('order-summary/', OrderSummary_V.as_view(), name='order-summary'),
    path('checkout', checkout.as_view(), name='checkout'),
    path('search/', search, name='search'),
    path('filter/', filter_V.as_view(), name='filter'),
    path('product-details/<slug>/',
         product_details_V.as_view(), name='product_details'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('contact', contact_us, name='contact_us'),
    path('my_account', my_account, name='my_account')
]
