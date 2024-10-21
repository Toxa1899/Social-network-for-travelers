from rest_framework import serializers
from .models import Country


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
