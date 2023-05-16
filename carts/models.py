from django.db import models

from products.models import ProductOption
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    