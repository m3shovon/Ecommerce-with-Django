from django.db import models
from django.conf import settings
# Create your models here.
from App_Shop.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # change_log
    # created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.quantity} X {self.item}'

    def get_total(self):
        total = self.item.price * self.quantity #item>Product>price
        float_total = format(total, '0.2f' ) # after decimal bit
        return float_total

#  Cart will show differnt items with quantity and price
#  but Order will show them at a single one on same chart


class Order(models.Model):
    order_items = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentId = models.CharField(max_length=264, blank=True, null=True)
    orederId = models.CharField(max_length=200, blank=True, null=True)

    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():
            total += float(order_item.get_total())
        return total