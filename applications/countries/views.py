from rest_framework import viewsets, status
from .models import Country
from django.db import models
from .serializers import CountriesSerializer
from rest_framework.permissions import (
    DjangoModelPermissionsOrAnonReadOnly,
    IsAuthenticated,
)
from permissions.permissions import IsNotBlocked, IsNotAdmin
from rest_framework.decorators import action
from applications.product.models import Post
from applications.product.serializers import PostSerializer
from rest_framework.response import Response
from config.mixins import GlobalContextMixin


class CountriesAllModelViewSet(GlobalContextMixin, viewsets.ModelViewSet):
    """
    Все страны , Get для всех , остальное только для  админов
    """

    permission_classes = [
        IsNotBlocked,
        DjangoModelPermissionsOrAnonReadOnly,
        IsAuthenticated,
    ]

    queryset = Country.objects.all()
    serializer_class = CountriesSerializer
    pagination_class = None


class CountriesModelViewSet(GlobalContextMixin, viewsets.ReadOnlyModelViewSet):
    """
    Список тех стран, для которых был создан один и более пост
    """

    permission_classes = [
        IsNotBlocked,
        IsNotAdmin,
        IsAuthenticated,
    ]
    serializer_class = CountriesSerializer
    queryset = (
        Country.objects.annotate(post_count=models.Count("posts"))
        .filter(post_count__gt=0)
        .order_by("name")
    )

    def retrieve(self, request, *args, **kwargs):
        """
        метод для фильтрации и вывода  стран
        """
        country = self.get_object()
        serializer = self.get_serializer(country)
        posts = Post.objects.filter(country=country, is_visible=True).order_by(
            "-created_at"
        )
        post_serializer = PostSerializer(posts, many=True)
        data = serializer.data
        data["posts"] = post_serializer.data
        return Response(data, status=status.HTTP_200_OK)
