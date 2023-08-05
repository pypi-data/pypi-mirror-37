from django.core.management import call_command
from django.core.management.base import BaseCommand
from fakenews.models import FactCheck, DisinformationType
from taggit.models import Tag
from fakenews.conf import settings

S3_UPLOAD_ROOT = settings.S3_UPLOAD_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("bake_data_feed")
        call_command("bake_web_context")

        for fc in FactCheck.objects.filter(status="pub"):
            call_command("bake_data_post", fc.id)

        for type in DisinformationType.objects.all():
            call_command("bake_data_type", type.label)

        for tag in Tag.objects.all():
            call_command("bake_data_tag", tag.slug)
