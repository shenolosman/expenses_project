from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

class Income(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    date = models.DateField(default=now)
    source = models.CharField(max_length=255)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ["-date"]


class IncomeSource(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Sources"
    def __str__(self):
        return self.name
