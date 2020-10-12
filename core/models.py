from django.conf import settings
from django.db import models
from django.shortcuts import reverse

label_choices = {
    ('N', 'New'),
    ('O', 'Out of Stock'),
    ('S', 'Sale')
}

category_choices = {
    ('M', ''),
    ('H', 'Home Decor'),
    ('A', 'Accessories'),
    ('T', 'Toys')
}

# The products


class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.FloatField()
    discounted = models.FloatField(blank=True, null=True)
    description = models.TextField()
    keywords = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="products", blank=True)
    label = models.CharField(choices=label_choices, max_length=1)
    category = models.CharField(choices=category_choices, max_length=1)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_abs_url(self):
        return reverse("core:product_details", kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


# Item in an order
class Order_Item(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

    def total_item_price(self):
        return self.quantity * self.item.cost

    def total_discount_item_price(self):
        return self.quantity * self.item.discounted

    def amount_saved(self):
        return self.total_item_price() - self.total_discount_item_price()

    def final_price(self):
        if self.item.discounted:
            return self.total_discount_item_price()
        return self.total_item_price()

# The items present in the cart, order


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(Order_Item)
    initial_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def total_amount(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        return total
