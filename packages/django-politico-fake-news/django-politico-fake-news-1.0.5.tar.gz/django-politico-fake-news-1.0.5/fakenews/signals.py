import savepagenow
from django.dispatch import receiver
from datetime import datetime
from taggit.models import Tag
from .models import Claim, FactCheck, DisinformationType
from fakenews.celery import (
    bake_feed_data,
    bake_post_data,
    unbake_post_data,
    bake_type_data,
    bake_tags_data,
    bake_web_context,
    bake_post_template,
    unbake_post_template,
)
from django.db.models.signals import (
    pre_save,
    post_save,
    pre_delete,
    post_delete,
)


@receiver(pre_save, sender=Claim)
def update_archive_url(sender, instance, **kwargs):
    prev = sender.objects.filter(pk=instance.pk).first()

    # Existing object
    if prev is not None:
        if instance.canoncial_url == "":
            instance.archive_url = ""
        elif instance.canoncial_url != prev.canoncial_url:
            instance.archive_url = savepagenow.capture_or_cache(
                instance.canoncial_url
            )[0]

    # New object
    else:
        instance.archive_url = savepagenow.capture_or_cache(
            instance.canoncial_url
        )[0]


@receiver(pre_save, sender=FactCheck)
def update_publish_date(sender, instance, **kwargs):
    if instance.status == "pub" and instance.publish_date is None:
        instance.publish_date = datetime.now()

    if not instance.status == "pub":
        instance.publish_date = None


@receiver(post_save, sender=FactCheck)
def bake_data(sender, instance, **kwargs):
    if instance.status == "pub":
        bake_post_data.delay(instance.id)
        bake_post_template.delay(instance.slug)

    if instance.status != "pub":
        unbake_post_data.delay(instance.id)
        unbake_post_template.delay(instance.slug)

    bake_feed_data.delay()
    bake_type_data.delay(instance.claim_reviewed.disinformation_type.label)
    bake_tags_data.delay([tag for tag in instance.claim_reviewed.tags.slugs()])


@receiver(post_delete, sender=FactCheck)
def unbake_data(sender, instance, **kwargs):
    if instance.status == "pub":
        unbake_post_data.delay(instance.id)
        unbake_post_template.delay(instance.slug)
        bake_feed_data.delay()
        bake_type_data.delay(instance.claim_reviewed.disinformation_type.label)
        bake_tags_data.delay(
            [tag for tag in instance.claim_reviewed.tags.slugs()]
        )


@receiver(post_save, sender=DisinformationType)
@receiver(post_delete, sender=DisinformationType)
@receiver(post_save, sender=Tag)
@receiver(post_delete, sender=Tag)
@receiver(post_save, sender=FactCheck)
def bake_context(sender, instance, **kwargs):
    bake_web_context.delay()
