from .models import Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев
    """

    class Meta:
        model = Comment
        fields = ["id", "content", "post"]
