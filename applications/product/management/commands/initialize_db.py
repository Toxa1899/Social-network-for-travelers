from django.core.management.base import BaseCommand
from applications.product.models import DaysOfWeek


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from applications.countries.tasks import country_task

        country_task.delay()
        data = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        for d in data:
            DaysOfWeek.objects.create(days_of_week=d)
