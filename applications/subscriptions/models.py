from django.db import models
from applications.countries.models import Country
from applications.product.models import Tag
from django.contrib.auth import get_user_model


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Страна",
    )
    tag = models.ForeignKey(
        Tag,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Тег",
    )
    subscribed_user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="followers",
        on_delete=models.CASCADE,
        verbose_name="подписанный пользователь",
    )

    class Meta:
        unique_together = ("user", "country", "tag", "subscribed_user")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
