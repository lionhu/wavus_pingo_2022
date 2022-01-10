from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from authentication.models import LoggedInUser
import logging

logger = logging.getLogger("error_logger")

__all__ = [
    "clear_unloggedin_users",
]


@shared_task
def clear_unloggedin_users():
    aware_time = make_aware(datetime.now())
    filters = {"created_at__lte": aware_time-timedelta(minutes=5)}

    users = LoggedInUser.objects.filter(**filters)
    if users.exists():
        for user in users:
            user.delete()


@periodic_task(run_every=(crontab(minute='*/5')))
def every_5minutes_tasks():
    clear_unloggedin_users.delay()
