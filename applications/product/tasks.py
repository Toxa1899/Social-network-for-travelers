from celery import shared_task
from .models import PostLiftSettings, LiftLog
from datetime import datetime, timedelta
from django.utils import timezone
import logging
import pytz

logger = logging.getLogger(__name__)


@shared_task
def lift_posts():
    logger.info("Task lift_posts called")
    now_utc = timezone.now()
    local_tz = pytz.timezone("Asia/Bishkek")
    now_local = now_utc.astimezone(local_tz)

    weekday = now_local.strftime("%A").lower()
    current_time = now_local.time()

    logger.info(f"Current time: {current_time}")
    logger.info(f"weekday: {weekday}")

    lift_settings = PostLiftSettings.objects.filter(
        start_date__lte=now_local.date(),
        end_date__gte=now_local.date(),
    )

    for setting in lift_settings:
        if setting.days_of_week.filter(days_of_week__iexact=weekday).exists():
            already_lifted_today = LiftLog.objects.filter(
                post=setting.post, timestamp__date=now_local.date()
            ).exists()
            if already_lifted_today:
                logger.info(f"Post {setting.post.id} already lifted today")
                continue

            lift_time = setting.time
            upper_bound = (
                datetime.combine(now_local.date(), lift_time)
                + timedelta(hours=1)
            ).time()

            logger.info(f"Lift time: {lift_time}, Upper bound: {upper_bound}")

            if lift_time <= current_time <= upper_bound:
                post = setting.post
                post.updated_at = now_local
                post.save()
                LiftLog.objects.create(post=post)
                logger.info(f"Post {post.id} lifted at {now_local}")
