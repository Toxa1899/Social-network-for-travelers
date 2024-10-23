from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum
from applications.product.models import Post, Tag
from applications.product.serializers import (
    LatestPostSerializer,
    TagSerializer,
)
from applications.account.serializers import TopUserSerializer
from rest_framework.authentication import get_user_model

User = get_user_model()


class GlobalContextMixin:
    def get_global_context_data(self):
        latest_posts = Post.objects.filter(is_visible=True).order_by(
            "-created_at"
        )[:3]
        tags = Tag.objects.annotate(post_count=Count("posts")).order_by(
            "-post_count"
        )[:10]
        top_users = User.objects.annotate(
            total_rating=Sum("ratings__rating")
        ).order_by("-total_rating")[:5]

        latest_posts_serializer = LatestPostSerializer(latest_posts, many=True)
        tags_serializer = TagSerializer(tags, many=True)
        top_users_serializer = TopUserSerializer(top_users, many=True)

        return {
            "latest_posts": latest_posts_serializer.data,
            "tags": tags_serializer.data,
            "top_users": top_users_serializer.data,
        }

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if isinstance(response.data, list):
            return Response(
                {"results": response.data, **self.get_global_context_data()}
            )
        response.data.update(self.get_global_context_data())
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data.update(self.get_global_context_data())
        return response
