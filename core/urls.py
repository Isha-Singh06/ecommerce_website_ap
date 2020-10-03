from django.urls import path
from .views import shop, Home_V, checkout, cart, product_details_V, contact_us

app_name = 'core'

urlpatterns = [
    path('', Home_V.as_view(), name = 'home'),
    path('index', Home_V.as_view(), name='home'),
    path('shop', shop, name='shop'),
    path('checkout', checkout, name='checkout'),
    path('shop-cart', cart, name='cart'),
    path('product-details/<slug>/', product_details_V.as_view(), name='product_details'),
    path('contact', contact_us, name='contact_us')
]