from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at", "content")
    search_fields = ("post__topic", "author__email", "content")
    list_filter = ("created_at",)
