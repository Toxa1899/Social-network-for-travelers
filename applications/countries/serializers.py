from rest_framework import serializers
from .models import Country


class CountriesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Сран
    """

    post_count = serializers.IntegerField(source="posts.count", read_only=True)

    class Meta:
        model = Country
        fields = ["id", "name", "description", "post_count"]
