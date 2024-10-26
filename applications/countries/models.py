from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Имя")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
