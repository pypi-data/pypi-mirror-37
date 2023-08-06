from raceratings.models import Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "label", "short_label", "order")


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "label", "short_label", "order")
