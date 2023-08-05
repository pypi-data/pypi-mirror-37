from django.core.management.base import BaseCommand
from fakenews.tasks.data_bakery import bake_web_context


class Command(BaseCommand):
    def handle(self, *args, **options):
        bake_web_context()
