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
    result_agricultura = models.FloatField(null=True, default=0)
    result_educacao = models.FloatField(null=True, default=0)
    result_ambiente = models.FloatField(null=True, default=0)
    result_saude = models.FloatField(null=True, default=0)
    result_infraestrutura = models.FloatField(null=True, default=0)
    result_desenvolvimento = models.FloatField(null=True, default=0)
    result_bancoCentral = models.FloatField(null=True, default=0)
    result_economia = models.FloatField(null=True, default=0)

    def __str__(self) -> str:
        return str(self.leader.name)


class Poll(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    bloc = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    pros = models.IntegerField(default=0)
    against = models.IntegerField(default=0)
    votes = models.JSONField(default=dict(votes=[]))
    has_open = models.BooleanField()
    coup = models.BooleanField(default=False, null=True)
