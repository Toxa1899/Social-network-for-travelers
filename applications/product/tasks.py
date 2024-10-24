from celery import shared_task
from .models import PostLiftSettings, LiftLog
from datetime import datetime, timedelta
import pytz


@shared_task
def lift_posts():
    print("Task lift_posts called")
    now = datetime.now(pytz.utc)
    weekday = now.strftime("%A").lower()
    current_time = now.time()

    lift_settings = PostLiftSettings.objects.filter(
        start_date__lte=now.date(),
        end_date__gte=now.date(),
    )
    # lift_settings = PostLiftSettings.objects.all()

    for setting in lift_settings:
        if weekday in setting.days_of_week:
            setting_time_with_tolerance = (
                datetime.combine(now.date(), setting.time)
                + timedelta(minutes=1)
            ).time()
            if setting.time <= current_time <= setting_time_with_tolerance:
                post = setting.post
                post.updated_at = now
                post.save()
                LiftLog.objects.create(post=post)
                print(f"Post {post.id} lifted at {now}")
