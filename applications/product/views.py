from rest_framework import viewsets, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Post, Rating, Comment
from permissions.permissions import (
    IsAuthorOrReadOnly,
    BlockCreatePosts,
    IsNotBlocked,
    IsNotAdmin,
)
from .serializers import (
    PostSerializer,
    CommentSerializer,
    PostDetailSerializer,
)
from .decorators import rating_schema, comment_schema
from applications.subscriptions.models import Subscription


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
        BlockCreatePosts,
        IsAuthenticated,
        IsNotBlocked,
        IsNotAdmin,
    ]
    queryset = Post.objects.filter(is_visible=True).order_by("-created_at")
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @rating_schema()
    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated]
    )
    def rating(self, request, pk=None, *args, **kwargs):
        rating_change = request.data.get("rating_change")
        if rating_change not in ["increase", "decrease"]:
            return Response(
                {
                    "error": "Недопустимое значение rating_change должен быть 'increase' or 'decrease'."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self._change_rating(request, rating_change)

    def _change_rating(self, request, rating_change):
        post = self.get_object()
        rating, created = Rating.objects.get_or_create(
            user=request.user, post=post
        )

        if created:
            rating.rating = 1 if rating_change == "increase" else -1
        else:
            return Response(
                {"rating": rating.rating}, status=status.HTTP_200_OK
            )

        rating.save()
        return Response(
            {"message": "success", "new_rating": rating.rating},
            status=status.HTTP_200_OK,
        )


class CommentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        IsAuthorOrReadOnly,
        IsNotBlocked,
        IsNotAdmin,
    ]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MainViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsNotBlocked, IsNotAdmin]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            subscriptions = Subscription.objects.filter(user=user)
            country_ids = subscriptions.values_list("country_id", flat=True)
            tag_ids = subscriptions.values_list("tag_id", flat=True)
            subscribed_user_ids = subscriptions.values_list(
                "subscribed_user_id", flat=True
            )

            queryset = (
                Post.objects.filter(
                    Q(is_visible=True),
                    Q(country_id__in=country_ids)
                    | Q(tags__id__in=tag_ids)
                    | Q(author_id__in=subscribed_user_ids),
                )
                .distinct()
                .order_by("-created_at")
            )
        else:
            queryset = Post.objects.filter(is_visible=True).order_by(
                "-created_at"
            )[:10]

        return queryset
