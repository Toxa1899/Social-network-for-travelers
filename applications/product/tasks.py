from celery import shared_task
from .models import PostLiftSettings, LiftLog
from datetime import datetime
import pytz


@shared_task
def lift_posts():
    now = datetime.now(pytz.utc)
    weekday = now.strftime("%A").lower()
    current_time = now.time()

    lift_settings = PostLiftSettings.objects.filter(
        start_date__lte=now.date(),
        end_date__gte=now.date(),
        time__lte=current_time,
    )

    for setting in lift_settings:
        if weekday in setting.days_of_week:
            post = setting.post
            post.updated_at = now
            post.save()
            LiftLog.objects.create(post=post)
            print(f"Post {post.id} lifted at {now}")
