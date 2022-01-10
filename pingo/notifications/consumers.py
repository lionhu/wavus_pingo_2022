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
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        if self.user:
            self.room_group_name = 'notification_{}_{}'.format(self.room_name, self.scope["user"].id)
            logger.error(f"room_group_name: {self.room_group_name}")
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            self.room_group_name = 'notification_broadcast_None'
            logger.error(f"room_group_name: {self.room_group_name}")
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        logger.error(text_data_json)
        logger.error(f"receive self.room_group_name: {self.room_group_name}")
        message_type = text_data_json['message_type']

        if self.user and message_type == 'heartbeat':
            Redis_key = settings.REDIS_KEYS["USER"]["LOGIN_STATUS"].format(self.scope["user"].id)
            cache.set(Redis_key, {'id': self.scope["user"].id,
                                  'usernmae': self.scope["user"].username,
                                  "last_beat": timezone.now()}
                      , 300)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'heartbeat',
                    'result': True,
                    "username": self.user.username
                }
            )
        elif message_type == 'public_broadcast':
            _data = {
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

            await self.channel_layer.group_send(
                'notification_{}_{}'.format(self.room_name, text_data_json['target']),
                _data
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                _data
            )

    async def heartbeat(self, event):
        await self.send(text_data=json.dumps({
            "heartbeat": "heartbeat",
            'result': event["result"],
            'username': event["username"]
        }))

    # Receive message from room group
    async def send_notification(self, event):
        logger.error("send_notification data")
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
            'target': target,
            'user': self.scope["user"].username,
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
