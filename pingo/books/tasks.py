from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab


# @shared_task
# def get_crypto_data():
#     print("get_crypto_data")
#
#
# @periodic_task(run_every=(crontab(minute='*/1')))
# def get_crypto_current():
#     print("periodic_task call get_crypto_current")
#     get_crypto_data.delay()
