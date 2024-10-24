from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
)

from .models import Comment
from permissions.permissions import (
    IsAuthorOrReadOnly,
    IsNotBlocked,
    IsNotAdmin,
)
from .serializers import (
    CommentSerializer,
)

from config.mixins import GlobalContextMixin


class CommentModelViewSet(GlobalContextMixin, viewsets.ModelViewSet):
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
