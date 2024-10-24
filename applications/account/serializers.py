import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError
from .models import BlockedUser
from applications.countries.models import Country
from applications.product.models import Post
from applications.product.serializers import PostSerializer

User = get_user_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RegisterSerializers(serializers.ModelSerializer):
    """
    Сериализатор для регистрации модели User.
    """

    password2 = serializers.CharField(
        min_length=8, required=True, write_only=True
    )

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        """
        Валидация паролей , точнее проверка на совпадение
        """
        p1 = attrs.get("password")
        p2 = attrs.pop("password2")

        if p1 != p2:
            raise serializers.ValidationError("Пароли не совпадают")

        try:
            validate_password(p1)
        except ValidationError as e:
            raise serializers.ValidationError({list(e.messages)})

        return attrs

    def create(self, validated_data):
        """
        create - создание пользователя
        """
        user = User.objects.create_user(**validated_data)
        return user


class DeleteAccountSerializer(serializers.Serializer):
    """
    Сериализатор для удаления аккаунта.
    """

    password = serializers.CharField(
        min_length=6, required=True, write_only=True
    )


class ChangePasswordSerializers(serializers.Serializer):
    """
    Сериализатор для смены пароля.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, password):
        """
        валидация текущего пароля
        """
        user = self.context["request"].user
        if not user.check_password(password):
            logger.warning(
                f"Неудачная попытка смены пароля для пользователя '{user.email}'. Неправильный старый пароль."
            )
            raise serializers.ValidationError("Пароль не совпадает с текущим")
        return password

    def validate(self, attrs):
        """
        валидация двух новых паролей
        """
        new_password = attrs.get("new_password")
        new_password_confirm = attrs.get("new_password_confirm")
        user = self.context["request"].user

        if new_password != new_password_confirm:
            logger.warning(
                f"Неудачная попытка смены пароля для пользователя '{user.email}'. Пароли не совпадают"
            )
            raise serializers.ValidationError("Пароли не совпадают")

        if user.check_password(new_password):
            logger.warning(
                f"Неудачная попытка смены пароля для пользователя '{user.email}'. Новый пароль совпадает с текущим"
            )
            raise serializers.ValidationError(
                "Новый пароль совпадает с текущим"
            )

        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def set_new_password(self):
        """
        метод для обновления пароля данный метод вызывается ,
        в представлении - views
        """
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save(update_fields=["password"])
        logger.info(f"Пароль для пользователя '{user.email}' был изменён")


class BlockedUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для  блокировке  (can_create_posts, is_blocked)
    """

    class Meta:
        model = BlockedUser
        fields = ["id", "user", "can_create_posts", "is_blocked"]


class UserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для  вывода пользователей
    """

    post_count = serializers.IntegerField(source="posts.count", read_only=True)
    country_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "post_count",
            "country_count",
        ]

    def get_country_count(self, obj):
        """
        количество стран, к которым пользователь создал посты
        """
        return Country.objects.filter(posts__author=obj).distinct().count()


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для  вывода пользователя >3
    """

    post_count = serializers.IntegerField(source="posts.count", read_only=True)
    country_count = serializers.SerializerMethodField()
    posts_by_country = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "post_count",
            "country_count",
            "posts_by_country",
        ]

    def get_country_count(self, obj):
        """
        количество стран, к которым пользователь создал посты
        """
        return Country.objects.filter(posts__author=obj).distinct().count()

    def get_posts_by_country(self, obj):
        """
        количество постов
        """
        posts = Post.objects.filter(author=obj).order_by(
            "country__name", "created_at"
        )
        country_posts = {}
        for post in posts:
            country_name = post.country.name
            if country_name not in country_posts:
                country_posts[country_name] = []
            country_posts[country_name].append(PostSerializer(post).data)
        return country_posts


class TopUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Топ пользователей
    """

    total_rating = serializers.IntegerField()

    class Meta:
        model = User
        fields = ["id", "email", "total_rating"]


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Пользователей
    """

    class Meta:
        model = User
        fields = ["id", "email"]
