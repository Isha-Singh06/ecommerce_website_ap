from django.urls import path
from .views import items_list, shop, Home_V, checkout, cart, product_details, contact_us

app_name = 'core'

urlpatterns = [
    path('', Home_V.as_view(), name = 'home'),
    path('index.html', items_list, name = 'items_list'),
    path('shop.html', shop, name='shop'),
    path('checkout.html', checkout, name='checkout'),
    path('shop-cart.html', cart, name='cart'),
    path('product-details.html', product_details, name='product_details'),
    path('contact.html', contact_us, name='contact_us')
]