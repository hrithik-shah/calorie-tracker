from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    name_id = models.CharField(max_length=200, blank=False, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name_id'],
                name="unique_food_name"
            )
        ]

