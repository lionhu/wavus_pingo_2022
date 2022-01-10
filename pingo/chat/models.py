from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.CharField(max_length=50, verbose_name='ルーム名')
    created_at = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, editable=False)


class Message(models.Model):
    room = models.ForeignKey(
        Room,
        related_name='messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, editable=False)
