from django.db.models.signals import post_save
from django.dispatch import receiver

from .celery import bake_api, bake_body_ratings, bake_feed
from .models import RaceRating, BodyRating


@receiver(post_save, sender=RaceRating)
def race_rating_save(sender, instance, **kwargs):
    bake_api()
    bake_feed()


@receiver(post_save, sender=BodyRating)
def body_rating_save(sender, instance, **kwargs):
    bake_body_ratings()
