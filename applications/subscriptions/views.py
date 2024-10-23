from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer
from django.db.models import Q
from rest_framework.response import Response
from permissions.permissions import IsNotBlocked, IsNotAdmin
from config.mixins import GlobalContextMixin


class SubscriptionViewSet(
    GlobalContextMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsNotBlocked, IsNotAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tag = serializer.validated_data.get("tag", None)
        country = serializer.validated_data.get("country", None)
        subscribed_user = serializer.validated_data.get(
            "subscribed_user", None
        )
        user = request.user

        existing_subscription = Subscription.objects.filter(
            Q(user=user),
            Q(tag=tag)
            | Q(country=country)
            | Q(subscribed_user=subscribed_user),
        ).first()

        if existing_subscription:
            existing_subscription.delete()
            return Response(
                {"message": "unsubscribe"}, status=status.HTTP_200_OK
            )
        else:
            serializer.save(user=user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "subscribe"},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)
