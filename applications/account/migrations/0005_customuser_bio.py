# Generated by Django 5.1.2 on 2024-10-20 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_customuser_is_blocked_alter_customuser_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
    ]
