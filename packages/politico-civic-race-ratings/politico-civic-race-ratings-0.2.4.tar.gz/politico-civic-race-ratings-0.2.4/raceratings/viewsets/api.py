from election.models import Race
from geography.models import Division, DivisionLevel
from government.models import Body
from itertools import chain, groupby
from rest_framework.response import Response
from rest_framework.views import APIView

from raceratings.models import Category
from raceratings.serializers import (
    RaceAPISerializer,
    BodyRatingSerializer,
    CategorySerializer,
    StateSerializer,
    DistrictSerializer,
    RaceRatingFeedSerializer,
)


class BodyRatingsViewSet(APIView):
    def get(self, request, format=None):
        data = []
        bodies = Body.objects.all()

        for body in bodies:
            latest_rating = body.ratings.latest("created_date")
            data.append(BodyRatingSerializer(latest_rating).data)

        return Response(data)


class RaceRatingsAPIViewSet(APIView):
    def get(self, request, format=None):
        races = Race.objects.filter(
            cycle__slug="2018", special=False
        ).order_by("office__division__label")

        minnesota = Race.objects.filter(
            cycle__slug="2018",
            special=True,
            office__division__label="Minnesota",
            office__body__slug="senate",
        )

        mississippi = Race.objects.filter(
            cycle__slug="2018",
            special=True,
            office__division__label="Mississippi",
            office__body__slug="senate",
        )

        races = races | minnesota | mississippi

        race_data = RaceAPISerializer(races, many=True).data

        return Response(race_data)


class RaceRatingsFeedViewSet(APIView):
    def get(self, request, format=None):
        races = Race.objects.filter(
            cycle__slug="2018", special=False
        ).order_by("office__division__label")

        minnesota = Race.objects.filter(
            cycle__slug="2018",
            special=True,
            office__division__label="Minnesota",
            office__body__slug="senate",
        )

        mississippi = Race.objects.filter(
            cycle__slug="2018",
            special=True,
            office__division__label="Mississippi",
            office__body__slug="senate",
        )

        races = races | minnesota | mississippi

        ratings = [race.ratings.order_by("created_date")[1:] for race in races]
        ratings = list(chain(*ratings))
        ratings = sorted(ratings, key=lambda r: r.created_date)
        grouped = {}
        for key, group in groupby(ratings, lambda r: r.created_date):
            date = key.strftime("%Y-%m-%d")

            grouped[date] = [
                RaceRatingFeedSerializer(rating).data for rating in list(group)
            ]

        return Response(grouped)


class RaceRatingsFilterViewSet(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        states = Division.objects.filter(level__name=DivisionLevel.STATE)
        districts = Division.objects.filter(level__name=DivisionLevel.DISTRICT)

        categories_data = CategorySerializer(categories, many=True).data
        states_data = StateSerializer(states, many=True).data
        districts_data = DistrictSerializer(districts, many=True).data

        data = {
            "categories": categories_data,
            "states": states_data,
            "districts": districts_data,
        }

        return Response(data)
