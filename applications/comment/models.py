from django.db import models
from applications.product.models import Post
from django.contrib.auth import get_user_model


User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
    )

    content = models.TextField(max_length=500, verbose_name="Текст")

    created_at = models.DateTimeField(
        auto_now_add=True, null=True, verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
