from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json
from django.conf import settings


class BroadcastNotification(models.Model):
    TYPE_CHOICES = (
        ('info', 'Information'),
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
    )
    message_type = models.CharField(choices=TYPE_CHOICES, max_length=32, default="info")
    target = models.IntegerField(default=0)  # 0 is public broadcasting news
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    hyper_link = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-broadcast_on"]


@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    if created:
        print("BroadcastNotification created")
        print(instance)
        #CrontabSchedule.objects.get_or_create use UTC as default, if USE-TZ=True wa set in settings,
        #here we should add timezone property to work properly
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.broadcast_on.hour,
                                                                  minute=instance.broadcast_on.minute,
                                                                  day_of_month=instance.broadcast_on.day,
                                                                  month_of_year=instance.broadcast_on.month,
                                                                  timezone=settings.CELERY_TIMEZONE)

        # because it is a periodic task, if we want to execute it just single time,
        # here we should add one_off=True to prevent it to be executed loopy.

        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-" + str(instance.id),
                                           task="notifications.tasks.broadcast_notification",
                                           one_off=True,
                                           args=json.dumps((instance.id,)),
                                           kwargs=json.dumps({
                                               'broadcast_notification_id': instance.id,
                                           }))
