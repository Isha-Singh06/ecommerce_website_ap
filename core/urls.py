from django.urls import path
from .views import shop, Home_V, checkout, cart, product_details_V, contact_us

app_name = 'core'

urlpatterns = [
    path('', Home_V.as_view(), name = 'home'),
    path('index.html', Home_V.as_view(), name='home'),
    path('shop.html', shop, name='shop'),
    path('checkout.html', checkout, name='checkout'),
    path('shop-cart.html', cart, name='cart'),
    path('product-details.html/<slug>/', product_details_V.as_view(), name='product_details'),
    path('contact.html', contact_us, name='contact_us')
]