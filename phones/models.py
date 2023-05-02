from django.db import models

from products.models import Product


class Phone(Product):
    field = models.CharField(max_length=255)