from django.contrib import admin

from .models import Item, Order_Item, Order, Reviews, Wishlist_Item, Wishlist

admin.site.register(Item)
admin.site.register(Order_Item)
admin.site.register(Order)
admin.site.register(Wishlist_Item)
admin.site.register(Wishlist)
admin.site.register(Reviews)
