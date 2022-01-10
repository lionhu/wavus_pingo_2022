from celery import shared_task
import time


@shared_task
def celery_task(counter):
    time.sleep(10)
    return '{} Done!'.format(counter)


@shared_task
def say_goodbye():
    return "Say goodbye to your"
