from rest_framework import generics

from raceratings.models import Category
from raceratings.serializers import CategoryListSerializer, CategorySerializer


class CategoryMixin(object):
    def get_queryset(self):
        return Category.objects.all()


class CategoryList(CategoryMixin, generics.ListAPIView):
    serializer_class = CategoryListSerializer


class CategoryViewSet(CategoryMixin, generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
