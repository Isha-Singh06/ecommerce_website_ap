from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, Order_Item, Order, Reviews
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Home page
class Home_V(ListView):
    model = Item
    paginate_by = 12
    template_name = 'index.html'

# Shopping cart
class OrderSummary_V(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


class checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

# Page to view all products
class shop_V(ListView):
    model = Item
    paginate_by = 27
    template_name = 'shop.html'


def cart(request):
    return render(request, "shop-cart.html")

# Page opened by clicking on an item, details displayed
def product_details_V(request, slug):
    item = get_object_or_404(Item, slug=slug)
    content = {
        'object': item
    }

    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 5)
        content = request.POST.get('content', '')
        review = Reviews.objects.create(product=item,user= request.user, stars= stars, content= content )
        return redirect("core:product_details", slug=slug)

    return render(request, 'product-details.html', content)


# Contact us page
def contact_us(request):
    return render(request, "contact.html")

# User's 'My Account' page
def my_account(request):
    return render(request, "my_account.html")

# Search for products (Autocomplete implementation ✔ )
def search(request):
    if request.method == 'GET':
        query= request.GET.get('q')


        if query is not None:
            lookups= Q(name__icontains=query) | Q(keywords__icontains=query)

            results= Item.objects.filter(lookups).distinct()

            context={'results': results,
                     'allProds' : Item.objects.all()}

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')

    else:
        return render(request, 'search.html')

# Filters
class filter_V(ListView):
    model = Item
    paginate_by = 27
    template_name = 'shop.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Item.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query) | Q(keywords__icontains=query)
        )
        return object_list

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    orderItem, created = Order_Item.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_q = Order.objects.filter(user=request.user, ordered=False)
    # To check whether an order exists already
    if order_q.exists():
        order = order_q[0]
        # To check if the item already exists in the order
        if order.items.filter(item__slug=item.slug).exists():
            orderItem.quantity += 1
            orderItem.save()
            messages.info(
                request, "The item has been added again, the item quantity has been increased in the cart")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item has been added to your cart")
            order.items.add(orderItem)
            return redirect("core:order-summary")
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=order_date)
        order.items.add(orderItem)
        messages.info(request, "This item has been added to your cart")
        return redirect("core:order-summary")


@login_required
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
            return redirect("core:order-summary")
        else:
            # Need to say that the item isnt in the order
            messages.info(request, "This item does not exist in your cart")
            return redirect("core:product_details", slug=slug)
    else:
        # Need to say that there is no order yet
        messages.info(request, "No items in your cart yet")
        return redirect("core:product_details", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
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
            if orderItem.quantity > 1:
                orderItem.quantity -= 1
                orderItem.save()
            else:
                order.items.remove(orderItem)

            messages.info(request, "This item quantity was updated")
            return redirect("core:order-summary")
        else:
            # Need to say that the item isnt in the order
            messages.info(request, "This item does not exist in your cart")
            return redirect("core:product_details", slug=slug)
    else:
        # Need to say that there is no order yet
        messages.info(request, "No items in your cart yet")
        return redirect("core:product_details", slug=slug)
