from rest_framework import viewsets, status
from .models import Post, Rating
from .serializers import PostSerializer
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.decorators import authentication_classes, action
from rest_framework.response import Response
from .decorators import rating_schema


class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().order_by("-created_at")
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

        rating, created = Rating.objects.get_or_create(
            user=self.request.user, post=self.get_object()
        )
        if created:
            if rating_change == "increase":
                rating.rating += 1
            elif rating_change == "decrease":
                rating.rating -= 1
        else:
            return Response(
                {"rating": rating.rating}, status=status.HTTP_200_OK
            )

        rating.save()
        return Response(
            {"message": "success", "new_rating": rating.rating},
            status=status.HTTP_200_OK,
        )
