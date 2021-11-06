from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    country = models.CharField(max_length=100, null=True, default=None)

class Bloc(models.Model):
    leader1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leader1")
    leader2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leader2")
    leader3 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leader3")
    leader4 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leader4")
