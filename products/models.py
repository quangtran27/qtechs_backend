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
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    order = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to="images/product/%Y/%m/%D")
