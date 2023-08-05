
import us
from geography.models import Division
from rest_framework import serializers


class DistrictSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return "{}-{}".format(obj.parent.code, obj.code)

    class Meta:
        model = Division
        fields = ("label", "id")


class StateSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    postal_code = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.code

    def get_postal_code(self, obj):
        return us.states.lookup(obj.code).abbr

    class Meta:
        model = Division
        fields = ("label", "id", "postal_code")
