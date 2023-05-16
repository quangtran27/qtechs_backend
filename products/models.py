from django.core.validators import RegexValidator
from django.db import models

from reviews.models import Review


class Brand(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images/brand/%Y/%m/%D")
    def __str__(self) -> str:
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/product-types/')
    path = models.CharField(max_length=100, validators=[RegexValidator(r'^[a-zA-Z\-]+$')])
    order = models.PositiveIntegerField()
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    priority = models.IntegerField(default=1)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    review = models.OneToOneField(Review, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f'{self.name}'

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    SKU = models.CharField(max_length=100, unique=True)
    on_sale = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()
    sold = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    color = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.summary}'

class SpecAttribute(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'

class OptionSpec(models.Model):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    attr = models.ForeignKey(SpecAttribute, on_delete=models.PROTECT)
    value = models.CharField(max_length=200)
    
class OptionImage(models.Model):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="images/product/%Y/%m/%D")
