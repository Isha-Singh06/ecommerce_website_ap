from django import template
from core.models import Order, Wishlist

register = template.Library()


@register.filter()
def cart_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.filter()
def wishlist_count(user):
    if user.is_authenticated:
        qs_wish = Wishlist.objects.filter(user=user, wishlist_present=False)
        if qs_wish.exists():
            return qs_wish[0].items.count()
    return 0
