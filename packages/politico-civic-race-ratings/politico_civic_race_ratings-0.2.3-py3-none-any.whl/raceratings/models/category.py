from django.db import models


class Category(models.Model):
    """
    A category of race ratings
    """

    label = models.CharField(max_length=50)
    short_label = models.CharField(max_length=30)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.label
