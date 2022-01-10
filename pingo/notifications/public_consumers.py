import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings

import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'public_notification'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logger.error(text_data_json)
        logger.error(f"public_notification receive self.room_group_name: {self.room_group_name}")
        message_type = text_data_json['message_type']

        if message_type == 'public_broadcast':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'send_notification',
                    "id": text_data_json['id'],
                    "icon": text_data_json['icon'],
                    "position": text_data_json['position'],
                    "message": text_data_json['message'],
                    "message_type": text_data_json['message_type'],
                    "read": text_data_json['read'],
                    "hyper_link": text_data_json['hyper_link'],
                    "timer": text_data_json['timer'],
                    "target": text_data_json['target'],
                }
            )

    # Receive message from room group
    async def send_notification(self, event):
        logger.error("public_notification send_notification data")
        logger.error(event)
        logger.error(type(event))
        id = event['id']
        icon = event['icon']
        position = event['position']
        message = event['message']
        message_type = event['message_type']
        read = event['read']
        hyper_link = event['hyper_link']
        timer = event['timer']
        target = event['target']

        await self.send(text_data=json.dumps({
            "public_notification": False,
            'id': id,
            'icon': icon,
            'position': position,
            'message': message,
            'message_type': message_type,
            'read': read,
            'hyper_link': hyper_link,
            'timer': timer,
            'target': target
        }))

    # @database_sync_to_async
    # def update_user_login_status(self, event):
    #     logger.error("update_user_login_status")
    #     logger.error(event)
    #     try:
    #         LoggedInUser.objects.update_or_create(user_id=self.scope["user"].id,
    #                                               defaults={"created_at": timezone.now(),
    #                                                         "ws_channel": True})
    #     except Exception as err:
    #         logger.error("Failed to update_user_login_status")
