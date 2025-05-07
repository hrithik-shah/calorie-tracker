from django.db import models
from .food import Food

class Item(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    calories = models.SmallIntegerField(blank=False, null=False)
    protein = models.SmallIntegerField(blank=False, null=False)
    carbohydrates = models.SmallIntegerField(default=None, blank=True, null=True)
    fats = models.SmallIntegerField(default=None, blank=True, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)