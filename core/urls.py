# All the urls that our website will require

from django.urls import path
from .views import shop_V, Home_V, Wishlist_V, my_account,my_orders, checkout,payment_View, search, OrderSummary_V, filter_V, product_details_V, remove_single_item_from_cart, contact_us, add_to_cart, remove_from_cart, add_to_wishlist, remove_from_wishlist, move_to_wishlist, move_to_cart

app_name = 'core'

urlpatterns = [
    path('', Home_V.as_view(), name='home'),
    path('index', Home_V.as_view(), name='home'),
    path('shop', shop_V.as_view(), name='shop'),
    path('order-summary/', OrderSummary_V.as_view(), name='order-summary'),
    path('wishlist/', Wishlist_V.as_view(), name='wishlist'),
    path('checkout', checkout.as_view(), name='checkout'),
    path('payment', payment_View.as_view(), name='payment'),
    path('search/', search, name='search'),
    path('filter/', filter_V.as_view(), name='filter'),
    path('product-details/<slug>/',
         product_details_V, name='product_details'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('move-to-cart/<slug>/', move_to_cart, name='move-to-cart'),
    path('add-to-wishlist/<slug>/', add_to_wishlist, name='add-to-wishlist'),
    path('move-to-wishlist/<slug>/', move_to_wishlist, name='move-to-wishlist'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-from-wishlist/<slug>/',
         remove_from_wishlist, name='remove-from-wishlist'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('contact', contact_us, name='contact_us'),
    path('my_account', my_account, name='my_account'),
    path('my_orders', my_orders, name='my orders')
]
