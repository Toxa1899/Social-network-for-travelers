from django.db import models
from applications.countries.models import Country
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Тег")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Страна",
    )
    topic = models.CharField(max_length=255, verbose_name="тема поста")

    body = models.TextField(
        validators=[MinLengthValidator(3)], verbose_name="Текст"
    )

    tags = models.ManyToManyField(
        Tag, blank=True, related_name="posts", verbose_name="Тег"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления"
    )
    is_visible = models.BooleanField(
        default=True, verbose_name="Виден ли пост"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostImage(models.Model):
    image = models.ImageField(
        upload_to="post_images/", max_length=255, verbose_name="Img"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_images",
        verbose_name="К какому посту относится Img",
    )

    class Meta:
        verbose_name = "Img поста"
        verbose_name_plural = "Img постов"


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Пользователь",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="ratings",
        verbose_name="Пост",
    )

    rating = models.SmallIntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Рейтинг",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )

    class Meta:
        unique_together = ("user", "post")
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинг"


class LiftLog(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="lift_logs"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Поднятие поста {self.post} в {self.timestamp}"

    class Meta:
        verbose_name = "Лог поднятия поста"
        verbose_name_plural = "Лог поднятия поста"


class DaysOfWeek(models.Model):
    days_of_week = models.CharField(max_length=50, verbose_name="дни недели")

    def __str__(self):
        return self.days_of_week


class PostLiftSettings(models.Model):
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE,
        related_name="lift_settings",
        verbose_name="Пост",
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата конца")
    time = models.TimeField(verbose_name="Время По KG")

    days_of_week = models.ManyToManyField(
        DaysOfWeek, verbose_name="дни недели "
    )

    def __str__(self):
        return f"Настройка поднятия для {self.post}"

    class Meta:
        verbose_name = "поднятие поста"
        verbose_name_plural = "поднятие поста"
