from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = ((1, "Nam"), (2, "Nữ"), (3, "Không muốn tiết lộ"))


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    address = models.CharField(max_length=255, blank=True)
