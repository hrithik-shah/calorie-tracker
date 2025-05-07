from django.db import models
from .food import Food

class Log(models.Model):
    food = models.ForeignKey(Food, on_delete=models.RESTRICT)
    timestamp = models.DateTimeField(blank=False, null=False)