from django.core.management import BaseCommand
from pingo.conf import settings as pingo_settings
import logging
from django.contrib.auth import get_user_model
from authentication.models import Profile, Client
from django_seed import Seed

logger = logging.getLogger("error_logger")
User = get_user_model()


class Command(BaseCommand):
    help = 'init Pingo Database'

    def handle(self, *args, **options):

        seeder = Seed.seeder()

        from store.models import Category
        seeder.add_entity(Category, 10)

        inserted_pks = seeder.execute()
