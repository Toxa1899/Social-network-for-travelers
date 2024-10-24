from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        from applications.countries.tasks import country_task

        country_task.delay()
