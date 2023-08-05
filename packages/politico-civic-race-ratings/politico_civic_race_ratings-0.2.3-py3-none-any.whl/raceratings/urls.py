from django.urls import path, re_path

from .views import Home, RacePage, RatingsEditor
from .viewsets import (
    BodyRatingsViewSet,
    RatingAdminView,
    RaceRatingsAPIViewSet,
    RaceRatingsFilterViewSet,
    RaceRatingsFeedViewSet,
)


urlpatterns = [
    path(Home.path, Home.as_view(), name=Home.name),
    re_path(RacePage.path, RacePage.as_view(), name=RacePage.name),
    path("ratings/edit", RatingsEditor.as_view(), name="raceratings-editor"),
    re_path(
        r"^api/ratings/$",
        RaceRatingsAPIViewSet.as_view(),
        name="raceratings_api_ratings-api",
    ),
    re_path(
        r"^api/filters/$",
        RaceRatingsFilterViewSet.as_view(),
        name="raceratings_api_filters-api",
    ),
    re_path(
        r"^api/feed/$",
        RaceRatingsFeedViewSet.as_view(),
        name="raceratings_api_feed-api",
    ),
    re_path(
        r"^api/body-ratings/$",
        BodyRatingsViewSet.as_view(),
        name="raceratings_api_body-ratings-api",
    ),
    re_path(
        r"^api/admin/ratings/$",
        RatingAdminView.as_view(),
        name="raceratings_api_ratings-admin",
    ),
]
