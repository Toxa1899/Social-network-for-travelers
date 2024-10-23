from rest_framework import serializers
from .models import Country


class CountriesSerializer(serializers.ModelSerializer):
    post_count = serializers.IntegerField(source="posts.count", read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "description", "post_count"]
