from django.core.management.base import BaseCommand
from fakenews.tasks.template_bakery import bake_post_template


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("post", type=str)

    def handle(self, *args, **options):
        bake_post_template(options["post"])
