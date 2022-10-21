from django.db import models
from django.contrib.auth.models import User

class Classes(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class Snack(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


def get_classes():
    return Classes.objects.get_or_create(name='deleted')[0]


class Child(models.Model):
    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=50)
    class_id = models.ForeignKey(Classes, on_delete=models.SET(get_classes))
    father = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    