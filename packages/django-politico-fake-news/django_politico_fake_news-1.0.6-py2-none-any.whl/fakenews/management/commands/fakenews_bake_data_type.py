from django.core.management.base import BaseCommand
from fakenews.tasks.data_bakery import bake_type_data


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('type', type=str)

    def handle(self, *args, **options):
        bake_type_data(options['type'])
