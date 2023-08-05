from django.contrib.postgres.fields import JSONField
from django.db import models
from election.models import Race


class DataProfile(models.Model):
    """
    A data profile of a division
    """
    race = models.ForeignKey(
        Race, on_delete=models.CASCADE, related_name='dataset'
    )
    data = JSONField()

    def __str__(self):
        return '{} profile'.format(self.race.label)
