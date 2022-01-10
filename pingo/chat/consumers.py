# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.db import transaction
from .signals import signalNewMessage
from .models import Message, Room
import logging

logger = logging.getLogger("error_logger")
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        if self.scope["user"].id:
            self.room_group_name = 'chat_%s' % str(self.scope["user"].id)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.disconnect(401)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']

        if self.scope["user"]:
            await self.createMessage(text_data_json)  # メッセージを DB に保存する
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': self.scope["user"].username,
        }))

    @database_sync_to_async
    def createMessage(self, event):
        logger.error(event)
        # signalNewMessage.send(None, message=event)
        try:
            if self.scope["user"].id:
                room, result = Room.objects.get_or_create(
                    name=self.room_group_name,
                    posted_by=self.scope["user"]
                )
                with transaction.atomic():
                    Message.objects.create(
                        room=room,
                        content=event['message'],
                        posted_by=self.scope["user"],
                    )
        except Exception as err:
            logger.error("Failed to create chat message")
