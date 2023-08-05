from django.core.management import call_command
from django.core.management.base import BaseCommand
from fakenews.views import WebHome, WebAbout, WebSubmit
from fakenews.models import FactCheck


class Command(BaseCommand):
    help = "Publishes our race pages"

    def bake_single_page(self, view):
        view.publish_statics()
        view.publish_serialized_data()
        view.publish_template()

    def handle(self, *args, **kwargs):
        call_command("collectstatic", "--noinput")

        self.bake_single_page(WebHome())
        self.bake_single_page(WebAbout())
        self.bake_single_page(WebSubmit())

        for fc in FactCheck.objects.filter(status="pub"):
            call_command("fakenews_bake_template_post", fc.slug)
