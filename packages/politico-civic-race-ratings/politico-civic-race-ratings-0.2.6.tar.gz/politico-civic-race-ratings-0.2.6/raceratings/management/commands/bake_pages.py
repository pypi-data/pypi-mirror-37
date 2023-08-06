import json

from django.core.management.base import BaseCommand
from election.models import Race
from geography.models import Division, DivisionLevel
from government.models import Body
from itertools import chain, groupby
from raceratings.models import Category
from raceratings.serializers import (
    BodyRatingSerializer,
    RaceAPISerializer,
    CategorySerializer,
    StateSerializer,
    DistrictSerializer,
    RaceRatingFeedSerializer,
)
from raceratings.utils.aws import defaults, get_bucket
from raceratings.views import Home, RacePage
from rest_framework.renderers import JSONRenderer
from tqdm import tqdm


class Command(BaseCommand):
    help = "Publishes our race pages"

    def bake_home_page(self):
        view = Home()
        view.publish_statics()
        view.publish_serialized_data()
        view.publish_template()

    def bake_body_ratings(self):
        data = []
        bodies = Body.objects.all()

        for body in bodies:
            latest_rating = body.ratings.latest("created_date")
            data.append(BodyRatingSerializer(latest_rating).data)

        json_string = JSONRenderer().render(data)
        key = "election-results/2018/race-ratings/data/body-ratings.json"
        print(">>> Publish data to: ", key)
        bucket = get_bucket()
        bucket.put_object(
            Key=key,
            ACL=defaults.ACL,
            Body=json_string,
            CacheControl=defaults.CACHE_HEADER,
            ContentType="application/json",
        )

    def bake_api(self, races):
        data = RaceAPISerializer(races, many=True).data
        json_string = JSONRenderer().render(data)  # noqa
        key = "election-results/2018/race-ratings/data/ratings.json"
        print(">>> Publish data to: ", key)
        bucket = get_bucket()
        bucket.put_object(
            Key=key,
            ACL=defaults.ACL,
            Body=json_string,
            CacheControl=defaults.CACHE_HEADER,
            ContentType="application/json",
        )

    def bake_filters(self):
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

        key = "election-results/2018/race-ratings/data/filters.json"
        print(">>> Publish data to: ", key)
        bucket = get_bucket()
        bucket.put_object(
            Key=key,
            ACL=defaults.ACL,
            Body=json.dumps(data),
            CacheControl=defaults.CACHE_HEADER,
            ContentType="application/json",
        )

    def bake_feed(self, races):
        ratings = [race.ratings.order_by("created_date")[1:] for race in races]
        ratings = list(chain(*ratings))
        ratings = sorted(ratings, key=lambda r: r.created_date)
        grouped = {}
        for key, group in groupby(ratings, lambda r: r.created_date):
            date = key.strftime("%Y-%m-%d")

            grouped[date] = [
                RaceRatingFeedSerializer(rating).data for rating in list(group)
            ]

        key = "election-results/2018/race-ratings/data/feed.json"
        print(">>> Publish data to: ", key)
        bucket = get_bucket()
        bucket.put_object(
            Key=key,
            ACL=defaults.ACL,
            Body=json.dumps(grouped),
            CacheControl=defaults.CACHE_HEADER,
            ContentType="application/json",
        )

    def bake_race_pages(self, races):
        stub = RacePage()
        stub.publish_statics()

        for race in tqdm(races):
            if race.office.division.level.name == DivisionLevel.DISTRICT:
                division = race.office.division.parent.slug
                code = race.office.division.code
            else:
                division = race.office.division.slug
                code = None

            if race.special:
                code = "special"

            if "governor" in race.office.slug:
                body = "governor"
            else:
                body = race.office.body.slug

            self.stdout.write("> {}".format(race.office.label))
            kwargs = {"division": division, "body": body, "code": code}

            view = RacePage(**kwargs)
            view.publish_serialized_data()
            view.publish_template(**kwargs)

    def handle(self, *args, **kwargs):
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

        self.bake_api(races)
        self.bake_feed(races)
        self.bake_filters()
        self.bake_body_ratings()

        self.bake_home_page()
        # self.bake_race_pages(races)
