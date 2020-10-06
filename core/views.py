from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Item, Order_Item, Order
from django.utils import timezone
from django.contrib import messages

class Home_V(ListView):
    model = Item
    paginate_by = 28
    template_name = 'index.html'

def shop(request):
    return render(request, "shop.html")

def checkout(request):
    return render(request, "checkout.html")

def cart(request):
    return render(request, "shop-cart.html")

class product_details_V(DetailView):
    model = Item
    template_name = "product-details.html"

def product_details(request):
    return render(request, "product-details.html")

def contact_us(request):
    return render(request, "contact.html")

def social_signup(request):
    return render(request, "./socialaccount/signup.html")

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    orderItem, created = Order_Item.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
    )
    order_q = Order.objects.filter(user=request.user, ordered=False)
    #To check whether an order exists already
    if order_q.exists():
        order = order_q[0]
        #To check if the item already exists in the order
        if order.items.filter(item__slug=item.slug).exists():
            orderItem.quantity += 1
            orderItem.save()
            messages.info(request, "The item has been added again, the item quantity has been increased in the cart")
            return redirect("core:product_details", slug=slug)

        else:
            messages.info(request, "This item has been added to your cart")
            order.items.add(orderItem)
            return redirect("core:product_details", slug=slug)
    else:
        order_date = timezone.now()
        order = Order.objects.create(user= request.user, order_date=order_date)
        order.items.add(orderItem)
        messages.info(request, "This item has been added to your cart")
        return redirect("core:product_details", slug=slug)




def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_q = Order.objects.filter(user=request.user, ordered=False)
    # To check whether an order exists already
    if order_q.exists():
        order = order_q[0]
        # To check if the item already exists in the order
        if order.items.filter(item__slug=item.slug).exists():
            orderItem = Order_Item.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(orderItem)
            messages.info(request, "This item has been removed from your cart")
            return redirect("core:product_details", slug=slug)
        else:
            # Need to say that the item isnt in the order
            messages.info(request, "This item does not exist in your cart")
            return redirect("core:product_details", slug=slug)
    else:
        # Need to say that there is no order yet
        messages.info(request, "No items in your cart yet")
        return redirect("core:product_details", slug=slug)



