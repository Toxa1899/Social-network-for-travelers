from django.contrib import admin
from .models import (
    Tag,
    Post,
    PostImage,
    Rating,
    LiftLog,
    PostLiftSettings,
)


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    max_num = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "author",
        "country",
        "topic",
        "body",
        "created_at",
        "updated_at",
        "is_visible",
    ]
    list_filter = ("is_visible", "created_at", "author", "country")
    search_fields = ("topic", "body", "author__email")
    inlines = [PostImageInline]
    ordering = ["-created_at"]
    list_editable = ("is_visible",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = (
        "name",
        "id",
    )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "rating", "created_at")
    search_fields = ("post__topic", "user__email")
    list_filter = ("created_at", "rating")


@admin.register(LiftLog)
class LiftLogAdmin(admin.ModelAdmin):
    list_display = ("post", "timestamp")
    search_fields = ("post__topic",)
    list_filter = ("timestamp",)


@admin.register(PostLiftSettings)
class PostLiftSettingsAdmin(admin.ModelAdmin):
    list_display = ("post", "start_date", "end_date", "time", "days_of_week")
    search_fields = ("post__topic",)


admin.site.register(PostImage)
