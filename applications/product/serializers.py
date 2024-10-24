from rest_framework import serializers
from .models import Post, PostImage, Tag, PostLiftSettings, LiftLog
from applications.comment.models import Comment
from applications.comment.serializers import CommentSerializer
from applications.countries.models import Country
from core.config import settings
from applications.account.models import CustomUser


class PostImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор  img для постов
    """

    class Meta:
        model = PostImage
        fields = ["image"]


class LatestPostSerializer(serializers.ModelSerializer):
    """
    Сериализатор последних постов
    """

    class Meta:
        model = Post
        fields = ["id", "topic", "created_at"]


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для тегов
    """

    class Meta:
        model = Tag
        fields = ["id", "name"]


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отображения постов
    """

    comment = CommentSerializer(source="comments", many=True)
    images = PostImageSerializer(
        source="post_images", many=True, read_only=True
    )
    tags = serializers.CharField(required=False)
    image_files = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "country",
            "topic",
            "body",
            "tags",
            "images",
            "image_files",
            "comment",
        ]

    def to_representation(self, instance):
        """
        для добавления поля (tags)
        """
        representation = super().to_representation(instance)
        representation["tags"] = [tag.name for tag in instance.tags.all()]
        return representation


class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для  отображения постов
    """

    author = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), required=False
    )
    images = PostImageSerializer(
        source="post_images", many=True, read_only=True
    )
    tags = serializers.CharField(required=False)
    image_files = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "author",
            "id",
            "country",
            "topic",
            "body",
            "tags",
            "images",
            "image_files",
        ]

    def validate_image_files(self, image_files):
        """
        валидация image
        """
        if image_files:
            if len(image_files) > 10:
                raise serializers.ValidationError(
                    "Количество изображений не может превышать 10 шт."
                )
            for i in image_files:
                filesize = int(i.size)
                if filesize > settings.MEGABYTE_LIMIT * 1024 * 1024:
                    raise serializers.ValidationError(
                        "Фотография весит больше 5мб."
                    )
        return image_files

    def create(self, validated_data):
        """
        Создание поста
        """
        tags_data = validated_data.pop("tags", None)
        image_files = validated_data.pop("image_files", None)

        post = Post.objects.create(**validated_data)

        self._create_images(post, image_files)
        self._create_tags(post, tags_data)

        return post

    def _create_images(self, post, image_files):
        """
        создание img
        """
        if image_files:
            for image in image_files:
                PostImage.objects.create(post=post, image=image)

    def _create_tags(self, post, tags_data):
        """
        создание тега
        """
        if tags_data:
            tag_names = tags_data.split()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                post.tags.add(tag)

    def to_representation(self, instance):
        """
        для добавления поля (tags)
        """
        representation = super().to_representation(instance)
        representation["tags"] = [tag.name for tag in instance.tags.all()]
        return representation


class PostLiftSettingSerializer(serializers.ModelSerializer):
    """
    Сериализатор для поднятия поста
    """

    class Meta:
        model = PostLiftSettings
        fields = "__all__"


class LiftLogSerializer(serializers.ModelSerializer):
    """
    Сериализатор для лога подгятия поста
    """

    class Meta:
        model = LiftLog
        fields = "__all__"
