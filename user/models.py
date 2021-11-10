from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    country = models.CharField(max_length=100, null=True, default=None)
    bloc = models.CharField(null=True, default=None, max_length=100)
    money = models.CharField(max_length=100, default='1000000000000')

    def __str__(self) -> str:
        return str(self.name)
