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
    """
    Представление подписки
    """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsNotBlocked, IsNotAdmin]

    def create(self, request, *args, **kwargs):
        """
        при повторном запросе если подписка существует ,
        выполняется отписка
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # получаем поля с сериализатора
        tag = serializer.validated_data.get("tag")
        country = serializer.validated_data.get("country")
        subscribed_user = serializer.validated_data.get("subscribed_user")

        user = request.user
        # фильтр по полям
        existing_subscription = Subscription.objects.filter(
            user=user,
            tag=tag if tag else None,
            country=country if country else None,
            subscribed_user=subscribed_user if subscribed_user else None,
        ).first()
        # если уже есть данный обьект то производится его удаление на выводе получаем unsubscribe
        if existing_subscription:
            existing_subscription.delete()
            return Response(
                {"message": "unsubscribe"}, status=status.HTTP_200_OK
            )

        # иначе создаем подписку
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
