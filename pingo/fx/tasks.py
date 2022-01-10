from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
import json
import requests
import datetime
from .models import Rate
import logging

logger = logging.getLogger("error_logger")


@shared_task
def update_fx_rate_db():
    url = "https://fx.dmm.com/api/fx/rate/rate.json"
    response = requests.get(url)
    response_data = json.loads(response.text)
    print(response_data)
    if response_data["meta"]["status"] == "OK":
        rates = response_data["body"]["rate"]
        for rate in rates:
            if rate[0] == "USD/JPY":
                created_at = datetime.datetime.strptime(rate[1], '%Y/%m/%d %H:%M:%S')
                bid = rate[2][0]
                ask = rate[3][0]
                high = rate[4]
                low = rate[5]
                logger.error(rate)
                Rate.objects.create(
                    currency_pare=rate[0],
                    bid=bid,
                    ask=ask,
                    high=high,
                    low=low,
                    created_at=created_at
                )


@periodic_task(run_every=(crontab(minute='*/5')))
def every_5_minutes_tasks():
    update_fx_rate_db.delay()
