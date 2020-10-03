from django.contrib import admin

from .models import Item, Order_Item, Order

admin.site.register(Item)
admin.site.register(Order_Item)
admin.site.register(Order)

