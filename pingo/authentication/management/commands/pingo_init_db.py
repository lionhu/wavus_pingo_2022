from django.core.management import BaseCommand
import logging
from django.contrib.auth import get_user_model
from store.models import Category, PointBank, Margin, OrderItem, Order,InventoryHistory,\
    ViewProductHistory, Favorite, Comment
from authentication.models import Profile

logger = logging.getLogger("error_logger")
User = get_user_model()


class Command(BaseCommand):
    help = 'init Pingo Database'
    access_public = {
        "superadmin": True,
        "supplier": False,
        "member": False,
        "staff": True
    }

    def init_order_related(self):
        Comment.objects.all().delete()
        Favorite.objects.all().delete()
        ViewProductHistory.objects.all().delete()
        InventoryHistory.objects.all().delete()
        PointBank.objects.all().delete()
        Margin.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Profile.objects.all().update(extra_info={})
        print("init_order_related")

    def handle(self, *args, **options):
        print("Initializing shop database")
        self.init_order_related()
        print("Shop database Initialized!")
