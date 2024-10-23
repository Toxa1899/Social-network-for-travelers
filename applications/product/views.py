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
from .serializers import PostSerializer, CommentSerializer
from .decorators import rating_schema, comment_schema


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
        BlockCreatePosts,
        IsNotBlocked,
        IsNotAdmin,
    ]
    queryset = Post.objects.filter(is_visible=True).order_by("-created_at")
    serializer_class = PostSerializer

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
