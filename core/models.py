from django.db import models

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