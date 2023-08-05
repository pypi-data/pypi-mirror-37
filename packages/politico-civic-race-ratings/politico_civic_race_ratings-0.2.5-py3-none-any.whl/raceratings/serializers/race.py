from django.core.exceptions import ObjectDoesNotExist
from election.models import Race, Election
from geography.models import DivisionLevel
from rest_framework import serializers
from rest_framework.reverse import reverse

from raceratings.models import RatingPageContent
from .candidate import CandidateSerializer
from .category import CategorySerializer
from .race_rating import RaceRatingSerializer, RaceRatingAdminSerializer


class RaceListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(
            "raceratings_api_race-detail",
            request=self.context["request"],
            kwargs={"pk": obj.pk},
        )

    class Meta:
        model = Race
        fields = ("url", "uid", "label")


class RaceAPISerializer(serializers.ModelSerializer):
    latest_rating = serializers.SerializerMethodField()
    candidates = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()

    def get_latest_rating(self, obj):
        try:
            latest = obj.ratings.latest("created_date")
            return CategorySerializer(latest.category).data
        except ObjectDoesNotExist:
            return None

    def get_candidates(self, obj):
        try:
            general_election = Election.objects.get(
                race=obj, election_day__date="2018-11-06"
            )

            candidates = general_election.get_candidates()
            return CandidateSerializer(candidates, many=True).data
        except:
            return []

    def get_label(self, obj):
        if not obj.office.body:
            label = obj.office.label
        else:
            if obj.office.body.slug == "senate":
                label = "{} Senate".format(obj.office.division.label)
            elif obj.office.body.slug == "house":
                label = "{}, District {}".format(
                    obj.office.division.parent.label,
                    obj.office.division.code
                    if not obj.office.division.code.endswith("00")
                    else "At-Large",
                )

        if obj.special:
            label = "{}, Special Election".format(label)

        return label

    def get_id(self, obj):
        # for easier search
        if obj.office.division.level.slug == DivisionLevel.DISTRICT:
            postal = obj.office.division.parent.code_components["postal"]
            code = obj.office.division.code
            return "{}-{}".format(postal, code)
        else:
            postal = obj.office.division.code_components["postal"]

            if obj.office.body:
                base = "{}-{}".format(postal, "sen")
                if obj.special:
                    return "{}-{}".format(base, "special")
                else:
                    return base
            else:
                return "{}-{}".format(postal, "gov")

    def get_body(self, obj):
        if obj.office.body:
            return obj.office.body.slug
        else:
            return "governor"

    def get_state(self, obj):
        if obj.office.division.level.name == DivisionLevel.DISTRICT:
            return obj.office.division.parent.code
        else:
            return obj.office.division.code

    def get_district(self, obj):
        if obj.office.division.level.name == DivisionLevel.DISTRICT:
            return "{}-{}".format(
                obj.office.division.parent.code, obj.office.division.code
            )
        else:
            return None

    class Meta:
        model = Race
        fields = (
            "latest_rating",
            "candidates",
            "label",
            "id",
            "body",
            "state",
            "district",
            "description",
        )


class RaceSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    office = serializers.SerializerMethodField()

    def get_ratings(self, obj):
        return RaceRatingSerializer(obj.ratings, many=True).data

    def get_content(self, obj):
        return RatingPageContent.objects.race_content(obj)

    def get_office(self, obj):
        if not obj.office.body:
            label = obj.office.label
        else:
            if obj.office.body.slug == "senate":
                label = "{} Senate".format(obj.office.division.label)
            elif obj.office.body.slug == "house":
                label = "{}, District {}".format(
                    obj.office.division.parent.label, obj.office.division.code
                )

        if obj.special:
            label = "{}, Special Election".format(label)

        return label

    class Meta:
        model = Race
        fields = ("uid", "ratings", "content", "office")


class RaceAdminSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField()
    office = serializers.SerializerMethodField()

    # a bunch of search fields
    abbrev = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_ratings(self, obj):
        return RaceRatingAdminSerializer(
            obj.ratings.order_by("created_date", "pk"), many=True
        ).data

    def get_office(self, obj):
        if obj.office.body and obj.office.body.slug == "senate":
            label = "{} {}".format(obj.office.division.label, "Senate")
        else:
            label = obj.office.label

        if obj.special:
            return "{} Special".format(label)
        else:
            return label

    def get_abbrev(self, obj):
        # for easier search
        if obj.office.division.level.slug == DivisionLevel.DISTRICT:
            postal = obj.office.division.parent.code_components["postal"]
            code = int(obj.office.division.code)
            return "{}-{}".format(postal, code)
        else:
            postal = obj.office.division.code_components["postal"]

            if obj.office.body:
                return "{}-{}".format(postal, "sen")
            else:
                return "{}-{}".format(postal, "gov")

    def get_code(self, obj):
        if obj.office.division.level.slug == DivisionLevel.DISTRICT:
            return int(obj.office.division.code)
        else:
            return 0

    class Meta:
        model = Race
        fields = ("uid", "ratings", "office", "abbrev", "code", "special")
