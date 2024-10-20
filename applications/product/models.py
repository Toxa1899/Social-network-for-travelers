from django.db import models
from applications.countries.models import Country
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.timezone import now

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=255)
    body = models.TextField(validators=[MinLengthValidator(3)])
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostImage(models.Model):
    image = models.ImageField(upload_to="post_images/", max_length=255)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_images"
    )

    def clean(self):
        if self.image.size > 5 * 1024 * 1024:
            raise ValidationError("Максимальный размер изображения: 5Мб")


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Rating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ratings"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="ratings"
    )

    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ("user", "post")


class LiftLog(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="lift_logs"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Поднятие поста {self.post} в {self.timestamp}"


class PostLiftSettings(models.Model):
    post = models.OneToOneField(
        Post, on_delete=models.CASCADE, related_name="lift_settings"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField()
    days_of_week = models.CharField(max_length=50)

    def __str__(self):
        return f"Настройка поднятия для {self.post}"
