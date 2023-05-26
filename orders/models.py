from django.db import models

from products.models import ProductOption
from users.models import User

ORDER_STATUS = ((1, 'Đã tạo đơn'), (2, 'Đang chuẩn bị'), (3, 'Đang giao hàng'), (4, 'Đã giao'), (5, 'Đã hủy'))
ORDER_PAYMENT = ((1, 'COD'), (2, 'Chuyển khoản ngân hàng'))

class Order(models.Model):
  user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='orders')
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  status = models.IntegerField(choices=ORDER_STATUS)
  customer_name = models.CharField(max_length=200)
  customer_phone = models.CharField(max_length=20)
  customer_address = models.CharField(max_length=255)
  payment = models.IntegerField(choices=ORDER_PAYMENT)
  shipping_fee = models.PositiveIntegerField(default=0)
  is_paid = models.BooleanField(default=False)
  is_reviewed = models.BooleanField(default=False)
  note = models.TextField(default='', blank=True)
  total = models.PositiveIntegerField()

  def __str__(self) -> str:
    return f'{self.created.strftime("%d-%m-%Y %H:%M")} - {self.customer_phone} - {self.customer_name}'

class OrderItem(models.Model):
  order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name='items')
  option = models.ForeignKey(to=ProductOption, on_delete=models.PROTECT)
  on_sale = models.BooleanField(default=False)
  price = models.PositiveIntegerField()
  sale_price = models.PositiveIntegerField()
  quantity = models.PositiveIntegerField()