from celery import shared_task
from .models import PostLiftSettings, LiftLog
from datetime import datetime, timedelta
import pytz
from django.utils import timezone


@shared_task
def lift_posts():
    print("Task lift_posts called")

    tz = pytz.timezone("Asia/Bishkek")
    now = datetime.now(tz)
    weekday = now.strftime("%A").lower()
    current_time = now.strftime("%H:%M")

    print(current_time)
    lift_settings = PostLiftSettings.objects.filter(
        start_date__lte=now.date(),
        end_date__gte=now.date(),
    )

    for setting in lift_settings:
        if setting.days_of_week.filter(days_of_week__iexact=weekday).exists():
            already_lifted_today = LiftLog.objects.filter(
                post=setting.post, timestamp__date=now.date()
            ).exists()
            if already_lifted_today:
                print(f"Post {setting.post.id} already lifted today")
                continue

            lift_time = datetime.combine(now.date(), setting.time).strftime(
                "%H:%M"
            )
            upper_bound = (
                datetime.combine(now.date(), setting.time) + timedelta(hours=1)
            ).strftime("%H:%M")

            if lift_time <= current_time <= upper_bound:
                post = setting.post
                post.updated_at = now
                post.save()
                LiftLog.objects.create(post=post)
                print(f"Post {post.id} lifted at {now}")
