from django.db import models
from government.models import Body
from raceratings.fields import MarkdownField

from .author import Author
from .category import Category


class BodyRating(models.Model):
    """
    An individual rating for a race
    """

    created_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        Author, on_delete=models.PROTECT, related_name="body_ratings"
    )
    body = models.ForeignKey(
        Body, on_delete=models.CASCADE, related_name="ratings"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="body_ratings"
    )
    explanation = MarkdownField(blank=True, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.body.label, self.category.short_label)
