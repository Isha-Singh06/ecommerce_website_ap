from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item

class Home_V(ListView):
    model = Item
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

