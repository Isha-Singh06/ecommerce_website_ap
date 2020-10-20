from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from .models import Item, Order_Item, Order, Reviews, Wishlist, Wishlist_Item, Address
from .forms import checkout_form
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

# Wishlist
class Wishlist_V(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            wishlist = Wishlist.objects.get(
                user=self.request.user, wishlist_present=False)
            context = {
                'object': wishlist
            }
            return render(self.request, "wishlist.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active wishlist")
            return redirect("/")

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid  

# Checkout page
class checkout(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        form = checkout_form()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'form': form
            }

            address_qs = Address.objects.filter(
                user=self.request.user, 
                default=True 
            )
            if address_qs.exists():
                context.update({ 'default_address': address_qs[0]})


            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = checkout_form(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_address = form.cleaned_data.get('use_default_address')
                if use_default_address:
                    print("Using the default address")
                    addresses_qs= Address.objects.filter(
                        user=self.request.user, 
                        default=True
                    )
                    if addresses_qs.exists():
                        house_address = addresses_qs[0]
                        order.address = house_address 
                        order.save()
                    else:
                        messages.info(self.request, "No default address available")
                        return redirect('core:checkout')
                else:
                    house_address = form.cleaned_data.get('house_address')
                    town = form.cleaned_data.get('town')
                    country = form.cleaned_data.get('country')
                    zip = form.cleaned_data.get('zip')
                    save_as_Default = form.cleaned_data.get('save_as_Default')


                    if is_valid_form([house_address, town, country, zip ]):
                        address = Address(
                            user=self.request.user,
                            house_address=house_address,
                            town=town,
                            country=country,
                            zip=zip

                        )
                        address.save()
                        order.address = address
                        order.save()

                        save_as_Default=form.cleaned_data.get('save_as_Default')
                        if save_as_Default:
                            addresses_qs = Address.objects.filter(
                                user=self.request.user,
                                default=True
                            )
                            if addresses_qs.exists():
                                for add in addresses_qs:
                                    add.default = False
                                    add.save()
                            address.default=True
                            address.save()
                            # address.default_true()
                    else: 
                        messages.info(self.request, "Please fill in the required fields")
                


                messages.success(self.request, "Almost Done")
                return redirect('core:payment')

            messages.info(self.request, "Failed Checkout")
            return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order_summary")

# Payment Page
class payment_View(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "payment.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user = self.request.user, ordered = False)
        order.ordered = True
        order.order_items_ordered()
        order.save()
        messages.success(self.request, "Your order was successful.")
        return redirect("/")



# Page to view all products
class shop_V(ListView):
    model = Item
    paginate_by = 27
    template_name = 'shop.html'
# Page opened by clicking on an item, details displayed

# The product detail page
def product_details_V(request, slug):
    item = get_object_or_404(Item, slug=slug)

    similar = Item.objects.filter(
        Q(category__icontains=item.category)).exclude(name=item.name)[:4]

    content = {
        'object': item,
        'similar': similar
    }

    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 5)
        content = request.POST.get('content', '')
        review = Reviews.objects.create(
            product=item, user=request.user, stars=stars, content=content)
        return redirect("core:product_details", slug=slug)

    return render(request, 'product-details.html', content)


# Contact us page
def contact_us(request):
    return render(request, "contact.html")

# User's 'My Account' page
def my_account(request):
    return render(request, "my_account.html")

# List of ordered items displayed
def my_orders(request):
        order = Order_Item.objects.filter(user=request.user,ordered=True)
        content = {
            'order':order
         }
        return render(request, "my_orders.html", content)

# User enabled to change default address
def change_address(request):
    address_qs = Address.objects.filter(user=request.user,
                                        default=True)
    if request.method == 'POST' and request.user.is_authenticated:
        if address_qs.exists():
            for add in address_qs:
                add.default = False
                add.save()
        house_address = request.POST.get('house_address')
        town = request.POST.get('Town')
        country = request.POST.get('Country')
        zip = request.POST.get('Zip')
        address = Address.objects.create(user=request.user, house_address=house_address, town=town, country=country,
                                         zip=zip, default=True)

        messages.success(request, "Your change was successful.")
        return redirect("/")

    if address_qs.exists():
        address_d = address_qs[0]
        content = {
            'address':address_d
        }
        return render(request, 'change_address.html', content)
    else:
        return render(request, 'change_address.html')


# Search for products (Autocomplete implementation ✔ )
def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if query is not None:
            lookups = Q(name__icontains=query) | Q(keywords__icontains=query) | Q(category__icontains=query) | Q(description__icontains=query)

            results = Item.objects.filter(lookups).distinct()

            context = {'results': results,
                       'allProds': Item.objects.all()}

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
            Q(name__icontains=query) | Q(description__icontains=query) | Q(
                category__icontains=query) | Q(keywords__icontains=query)
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
def move_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    # removing from wishlist
    wishlist_q = Wishlist.objects.filter(
        user=request.user, wishlist_present=False)
    # To check whether a wishlist exists already
    if wishlist_q.exists():
        wishlist = wishlist_q[0]
        # To check if the item already exists in the wishlist

        wishlistItem = Wishlist_Item.objects.filter(
            item=item,
            user=request.user,
            wishlist_present=False
        )[0]
        wishlist.items.remove(wishlistItem)
        item.wishlist_counter = item.wishlist_counter - 1
        item.save()

    # adding to cart
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
            messages.info(
                request, "The item is already in your cart")
            return redirect("core:order-summary")

        else:
            messages.info(request, "This item has been moved to your cart")
            order.items.add(orderItem)
            return redirect("core:order-summary")
    else:
        order_date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=order_date)
        order.items.add(orderItem)
        messages.info(request, "This item has been moved to your cart")
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


@login_required
def add_to_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wishlistItem, created = Wishlist_Item.objects.get_or_create(
        item=item,
        user=request.user,
        wishlist_present=False
    )
    wishlist_q = Wishlist.objects.filter(
        user=request.user, wishlist_present=False)
    # To check whether a wishlist exists already
    if wishlist_q.exists():
        wishlist = wishlist_q[0]
        # To check if the item already exists in the wishlist
        if wishlist.items.filter(item__slug=item.slug).exists():
            messages.info(
                request, "The item already exists in your wishlist")
            return redirect("core:wishlist")

        else:
            item.wishlist_counter = item.wishlist_counter + 1
            item.save()
            messages.info(request, "This item has been added to your wishlist")
            wishlist.items.add(wishlistItem)
            return redirect("core:wishlist")
    else:
        order_date = timezone.now()
        wishlist = Wishlist.objects.create(
            user=request.user, order_date=order_date)
        wishlist.items.add(wishlistItem)
        item.wishlist_counter = item.wishlist_counter + 1
        item.save()
        messages.info(request, "This item has been added to your wishlist")
        return redirect("core:wishlist")


@login_required
def move_to_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_q = Order.objects.filter(user=request.user, ordered=False)
    # To check whether an order exists already
    if order_q.exists():
        order = order_q[0]
        # To check if the item already exists in the order

        orderItem = Order_Item.objects.filter(
            item=item,
            user=request.user,
            ordered=False
        )[0]
        order.items.remove(orderItem)

    wishlistItem, created = Wishlist_Item.objects.get_or_create(
        item=item,
        user=request.user,
        wishlist_present=False
    )
    wishlist_q = Wishlist.objects.filter(
        user=request.user, wishlist_present=False)
    # To check whether a wishlist exists already
    if wishlist_q.exists():
        wishlist = wishlist_q[0]
        # To check if the item already exists in the wishlist
        if wishlist.items.filter(item__slug=item.slug).exists():
            messages.info(
                request, "The item already exists in your wishlist")
            return redirect("core:wishlist")

        else:
            item.wishlist_counter = item.wishlist_counter + 1
            item.save()
            messages.info(request, "This item has been moved to your wishlist")
            wishlist.items.add(wishlistItem)
            return redirect("core:wishlist")
    else:
        order_date = timezone.now()
        wishlist = Wishlist.objects.create(
            user=request.user, order_date=order_date)
        wishlist.items.add(wishlistItem)
        item.wishlist_counter = item.wishlist_counter + 1
        item.save()
        messages.info(request, "This item has been moved to your wishlist")
        return redirect("core:wishlist")


@login_required
def remove_from_wishlist(request, slug):
    item = get_object_or_404(Item, slug=slug)
    wishlist_q = Wishlist.objects.filter(
        user=request.user, wishlist_present=False)
    # To check whether a wishlist exists already
    if wishlist_q.exists():
        wishlist = wishlist_q[0]
        # To check if the item already exists in the wishlist
        if wishlist.items.filter(item__slug=item.slug).exists():
            wishlistItem = Wishlist_Item.objects.filter(
                item=item,
                user=request.user,
                wishlist_present=False
            )[0]
            wishlist.items.remove(wishlistItem)
            item.wishlist_counter = item.wishlist_counter - 1
            item.save()
            messages.info(
                request, "This item has been removed from your wishlist")
            return redirect("core:wishlist")
        else:
            # Need to say that the item isnt in the order
            messages.info(request, "This item does not exist in your wishlist")
            return redirect("core:wishlist", slug=slug)
    else:
        # Need to say that there is no order yet
        messages.info(request, "No items in your wishlist yet")
        return redirect("core:wishlist", slug=slug)
