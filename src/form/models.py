from django.db import models
from user.models import User

class Form(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField()
    questions = models.JSONField()
    weight = models.IntegerField(default=1)

    def __str__(self) -> str:
        return str(self.name)

class Answer(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    leader = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.JSONField()
    result_agricultura = models.IntegerField(null=True)
    result_educacao = models.IntegerField(null=True)
    result_ambiente = models.IntegerField(null=True)
    result_saude = models.IntegerField(null=True)
    result_infraestrutura = models.IntegerField(null=True)
    result_desenvolvimento = models.IntegerField(null=True)
    result_bancoCentral = models.IntegerField(null=True)
    result_economia = models.IntegerField(null=True)

    def __str__(self) -> str:
        return str(self.leader.name)

class Poll(models.Model):
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    bloc = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    pros = models.IntegerField()
    against = models.IntegerField()
    votes = models.JSONField()
    has_open = models.BooleanField()
