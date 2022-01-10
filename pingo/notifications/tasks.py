from celery import shared_task
from channels.layers import get_channel_layer
from .models import BroadcastNotification
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from django_celery_beat.models import PeriodicTask
from celery.exceptions import Ignore
import asyncio
import traceback


@periodic_task(run_every=(crontab(hour='*/1')))
def cleanup_broadcast_notifications():
    notifications = PeriodicTask.objects.filter(name__istartswith="broadcast").all()

    if notifications.count() > 0:
        for notification in notifications:
            broadcast_notification_id = int(notification.name.split("-")[2])
            broadcast_notification_obj = BroadcastNotification.objects.filter(pk=broadcast_notification_id).first()
            if broadcast_notification_obj is not None and broadcast_notification_obj.sent:
                notification.delete()


@shared_task(bind=True)
def broadcast_notification(self, *args, **kwargs):
    print(args)
    print(kwargs)
    try:
        notification = BroadcastNotification.objects.filter(id=int(kwargs["broadcast_notification_id"]))
        if len(notification) > 0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notification_broadcast",
                {
                    'type': 'send_notification',
                    # notification data sent to user
                    'id': notification.id,
                    'message': notification.message,
                    'message_type': notification.message_type,
                    'read': notification.read,
                    'hyper_link': notification.hyper_link,
                    'target': notification.target,
                }))
            notification.sent = True
            notification.save()
            return 'Done'

        else:
            self.update_state(
                state='FAILURE',
                meta={'exe': "Not Found"}
            )

            raise Ignore()

    except Exception as ex:
        self.update_state(
            state='FAILURE',
            meta={
                'exe': "Failed",
                'exc_type': type(ex).__name__,
                'exc_message': traceback.format_exc().split('\n')
                # 'custom': '...'
            }
        )

        raise Ignore()
