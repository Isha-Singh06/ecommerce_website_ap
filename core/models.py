from django.conf import  settings
from django.db import models

#The products
class Item(models.Model):
    name = models.CharField(max_length=50)
    cost = models.FloatField()
    def __str__(self):
        return self.name

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