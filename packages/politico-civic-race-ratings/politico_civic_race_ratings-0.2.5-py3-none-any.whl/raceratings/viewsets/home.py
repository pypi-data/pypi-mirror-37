from election.models import Race
from geography.models import Division, DivisionLevel
from rest_framework.views import APIView
from rest_framework.response import Response

from raceratings.models import (BadgeType, Category, RaceBadge,
                                RatingPageContent)
from raceratings.serializers import (RaceHomeSerializer,
                                     CategorySerializer,
                                     BadgeTypeSerializer,
                                     RaceBadgeHomeSerializer,
                                     DivisionSerializer)


class HomeView(APIView):
    def get(self, request, format=None):
        races = Race.objects.filter(cycle__slug='2018').order_by(
            'office__label'
        )
        race_data = RaceHomeSerializer(races, many=True).data

        categories = Category.objects.all()
        categories_data = CategorySerializer(categories, many=True).data

        badges = RaceBadge.objects.all()
        badges_data = RaceBadgeHomeSerializer(badges, many=True).data

        badge_types = BadgeType.objects.all()
        badge_types_data = BadgeTypeSerializer(badge_types, many=True).data

        divisions = Division.objects.filter(level__name=DivisionLevel.STATE)
        divisions_data = DivisionSerializer(divisions, many=True).data

        content = RatingPageContent.objects.home_content()

        context = {
            'races': race_data,
            'categories': categories_data,
            'badges': badges_data,
            'badge_types': badge_types_data,
            'divisions': divisions_data,
            'content': content
        }

        return Response(context)
