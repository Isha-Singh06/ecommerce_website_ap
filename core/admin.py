from django.contrib import admin

from .models import Item, order_Item, order

admin.site.register(Item)
admin.site.register(order_Item)
admin.site.register(order)

