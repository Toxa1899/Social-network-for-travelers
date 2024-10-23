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


class CountriesAllModelViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [
        IsNotBlocked,
        IsNotAdmin,
        IsAuthenticated,
    ]

    queryset = Country.objects.all()
    serializer_class = CountriesSerializer


class CountriesModelViewSet(viewsets.ReadOnlyModelViewSet):
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
    pagination_class = None

    def retrieve(self, request, *args, **kwargs):
        country = self.get_object()
        serializer = self.get_serializer(country)
        posts = Post.objects.filter(country=country, is_visible=True).order_by(
            "-created_at"
        )
        post_serializer = PostSerializer(posts, many=True)
        data = serializer.data
        data["posts"] = post_serializer.data
        return Response(data, status=status.HTTP_200_OK)
