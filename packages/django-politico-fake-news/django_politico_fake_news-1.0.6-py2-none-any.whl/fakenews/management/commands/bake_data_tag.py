from django.core.management.base import BaseCommand
from fakenews.tasks.data_bakery import bake_tags_data


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('tag', type=str)

    def handle(self, *args, **options):
        bake_tags_data(options['tag'])
