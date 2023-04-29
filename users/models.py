from django.db import models

GENDER_CHOICES = ((1, "Nam"), (2, "Nữ"), (3, "Không muốn tiết lộ"))


class User(models.Model):
    name = models.CharField(max_length=100, default="Tên khách hàng")
    phone = models.CharField(max_length=20, unique=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    password = models.CharField(max_length=200)
    email = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.phone
