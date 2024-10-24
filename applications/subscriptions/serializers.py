from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ["country", "tag", "subscribed_user"]

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "Необходимо указать одно из значений (country, tag, subscribed_user)"
            )

        if len(attrs.keys()) > 1:
            raise serializers.ValidationError("Указано больше одного значения")

        return attrs
