from django.core.management.base import BaseCommand
from fakenews.tasks.data_bakery import bake_post_data


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('post', type=str)

    def handle(self, *args, **options):
        bake_post_data(options['post'])
