from django.contrib import admin

from election.models import Race
from raceratings.models import (
    Author,
    BodyRating,
    Category,
    DataProfile,
    RatingPageContent,
    RaceRating,
)

from .race import RaceAdmin
from .page_content import PageContentAdmin
from .race_rating import RaceRatingAdmin

admin.site.register(Author)
admin.site.register(BodyRating)
admin.site.register(Category)
admin.site.register(DataProfile)
admin.site.unregister(Race)
admin.site.register(Race, RaceAdmin)
admin.site.register(RatingPageContent, PageContentAdmin)
admin.site.register(RaceRating, RaceRatingAdmin)
