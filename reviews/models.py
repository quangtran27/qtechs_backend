from django.db import models

from users.models import User


class Review(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateField(auto_now=True)
    updated = models.DateField()

    def __str__(self) -> str:
        return f'{self.title} - {self.user.name}'
