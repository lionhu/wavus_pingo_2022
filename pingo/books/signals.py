from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tag


@receiver(post_save,sender=Tag)
def refresh_all_books_tag(sender,instance,created,*args, **kwargs):
    if created:
        print("refresh_all_books_tag, Tag created")
