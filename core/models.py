from django.conf import  settings
from django.db import models
from django.shortcuts import reverse

label_choices = {
    ('N','New'),
    ('O','Out of Stock'),
    ('S','Sale')
}

category_choices = {
    ('M',''),
    ('H','Home Decor'),
    ('A','Accessories'),
    ('T','Toys')
}

#The products
class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.FloatField()
    label = models.CharField(choices=label_choices, max_length=1)
    category = models.CharField(choices=category_choices, max_length=1)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_abs_url(self):
        return reverse("core:product_details", kwargs={
            'slug': self.slug
        } )

#Item in an order
class order_Item(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#The items present in the cart, order
class order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(order_Item)
    inital_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username