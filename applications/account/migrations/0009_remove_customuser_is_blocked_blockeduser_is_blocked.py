# Generated by Django 5.1.2 on 2024-10-23 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_remove_customuser_create_posts_blockeduser"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="is_blocked",
        ),
        migrations.AddField(
            model_name="blockeduser",
            name="is_blocked",
            field=models.BooleanField(default=False),
        ),
    ]
