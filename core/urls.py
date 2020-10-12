from django.urls import path
from .views import shop_V, Home_V, checkout, cart, OrderSummary_V, search_V,filter_V, product_details_V, remove_single_item_from_cart, contact_us, add_to_cart, remove_from_cart, social_signup

app_name = 'core'

urlpatterns = [
    path('', Home_V.as_view(), name='home'),
    path('index', Home_V.as_view(), name='home'),
    path('shop', shop_V.as_view(), name='shop'),
    path('checkout', checkout, name='checkout'),
    path('order-summary/', OrderSummary_V.as_view(), name='order-summary'),
    path('shop-cart', cart, name='cart'),
    path('search/', search_V.as_view(), name='search'),
    path('filter/', filter_V.as_view(), name='filter'),
    path('product-details/<slug>/',
         product_details_V.as_view(), name='product_details'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    path('contact', contact_us, name='contact_us'),
    path('social_signup', social_signup, name='social_signup')
]
