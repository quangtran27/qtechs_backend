from django.db import models

from reviews.models import Review


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/brand/%Y/%m/%D")

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    review = models.OneToOneField(Review, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
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

    def __str__(self) -> str:
        return f'{self.laptop.name} {self.ram}-{self.storage}-{self.color}' 

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="images/product/%Y/%m/%D")
