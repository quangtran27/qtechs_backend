from django.db import models


class Banner(models.Model):
	order = models.IntegerField(default=1)
	image = models.ImageField(upload_to='images/banners/%Y/%m/%D')
	url = models.URLField(max_length=500)