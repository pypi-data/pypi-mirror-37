from rest_framework import serializers

from raceratings.models import BodyRating
from .category import CategorySerializer


class BodyRatingSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()

    def get_category(self, obj):
        return CategorySerializer(obj.category).data

    def get_body(self, obj):
        return obj.body.slug

    class Meta:
        model = BodyRating
        fields = ("created_date", "category", "explanation", "body")
