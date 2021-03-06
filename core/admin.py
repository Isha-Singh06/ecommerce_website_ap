from django.contrib import admin

from .models import Item, Order_Item, Order, Reviews, Wishlist_Item, Wishlist, Address  

class AddressAdmin(admin.ModelAdmin):
    list_display=[
        'user',
        'house_address',
        'town',
        'country',
        'zip', 
        'default' 
    ]
    list_filter=[ 'default', 'country' ]
    search_fields= [ 'uesr', 'house_address', 'zip']



admin.site.register(Item)
admin.site.register(Order_Item)
admin.site.register(Order)
admin.site.register(Wishlist_Item)
admin.site.register(Wishlist)
admin.site.register(Reviews)
admin.site.register(Address, AddressAdmin)



