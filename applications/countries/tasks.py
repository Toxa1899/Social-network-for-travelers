import requests
from core.config import settings
from applications.countries.models import Country
import logging
from celery import shared_task


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@shared_task
def country_task():
    url = f"https://api.countrylayer.com/v2/all?access_key={settings.ACCESS_KEY.get_secret_value()}"
    response = requests.get(url)
    result = response.json()
    print(result)
    for r in result:
        country_name = r.get("name", None)
        if country_name:
            _, created = Country.objects.get_or_create(name=country_name)
            if created:
                logger.info(f"Добавлена новая страна {country_name}")
