from django.db import models

from products.models import Product


# Create your models here.
class Laptop(Product):
    pass

class LaptopConfig(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='configs')
    screen = models.CharField(max_length=100)
    battery = models.CharField(max_length=10)
    cpu = models.CharField(max_length=100)
    gpu = models.CharField(max_length=100)
    ram = models.PositiveSmallIntegerField()
    storage = models.PositiveSmallIntegerField()
    quantity = models.PositiveIntegerField()
    sold = models.PositiveIntegerField()
    on_sale = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()
    color = models.CharField(max_length=100)
    summary = models.CharField(max_length=255, default='')

    def __str__(self) -> str:
        return f'{self.laptop.name} {self.ram}-{self.storage}-{self.color}' 