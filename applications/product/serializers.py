from rest_framework import serializers
from .models import Post, PostImage, Tag
from applications.countries.models import Country


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ["image"]


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(
        source="post_images", many=True, read_only=True
    )
    tags = serializers.CharField(required=False)
    image_files = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Post
        fields = ["country", "topic", "body", "tags", "images", "image_files"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", None)
        image_files = validated_data.pop("image_files", None)

        post = Post.objects.create(**validated_data)

        self._create_images(post, image_files)
        self._create_tags(post, tags_data)

        return post

    def _create_images(self, post, image_files):
        if image_files:
            for image in image_files:
                PostImage.objects.create(post=post, image=image)

    def _create_tags(self, post, tags_data):
        if tags_data:
            for t in tags_data.split(" "):
                tag, _ = Tag.objects.get_or_create(name=t)
                post.tags.add(tag)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["tags"] = [tag.name for tag in instance.tags.all()]
        return representation
