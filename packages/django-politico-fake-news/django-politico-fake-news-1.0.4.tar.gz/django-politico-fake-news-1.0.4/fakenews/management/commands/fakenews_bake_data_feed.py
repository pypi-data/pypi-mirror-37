from django.core.management.base import BaseCommand
from fakenews.tasks.data_bakery import bake_feed_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        bake_feed_data()
