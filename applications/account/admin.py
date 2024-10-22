from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdminModel(admin.ModelAdmin):
    list_display = ("id", "email")


# Register your models here.

# admin.site.register(CustomUser)
