# Generated by Django 5.1.2 on 2024-10-21 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0008_alter_post_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="title",
            new_name="topic",
        ),
    ]
