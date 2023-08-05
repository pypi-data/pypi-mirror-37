import logging
import math
import os
from celery import shared_task
from taggit.models import Tag
from .aws import publish_to_aws, remove_from_aws
from ..models import FactCheck, DisinformationType
from ..serializers import (
    FactCheckFeedSerializer,
    FactCheckArticleSerializer,
    DisinformationTypeContextSerializer,
)
from ..conf import settings


S3_UPLOAD_ROOT = settings.S3_UPLOAD_ROOT
S3_STATIC_ROOT = settings.S3_STATIC_ROOT
POSTS_PER_PAGE = 5

logger = logging.getLogger("tasks")


def paginate(queryset, filepath):
    sets = []
    page_count = math.ceil(len(queryset) / POSTS_PER_PAGE)
    for page in range(0, page_count):
        limit = page * POSTS_PER_PAGE
        offset = (page + 1) * POSTS_PER_PAGE
        page_subset = queryset[limit:offset]
        serialized_page = FactCheckFeedSerializer(page_subset, many=True)
        sets.append(serialized_page.data)

    directory_path = os.path.join(S3_UPLOAD_ROOT, filepath)
    static_path = os.path.join(S3_STATIC_ROOT, directory_path)
    output = []
    for idx, page in enumerate(sets):
        name = "set-{}.json".format(idx + 1)
        url = os.path.join(static_path, name)
        next = (
            "{}/set-{}.json".format(static_path, idx + 2)
            if idx + 1 < len(sets)
            else None
        )
        prev = "{}/set-{}.json".format(static_path, idx) if idx > 0 else None
        file_upload_path = os.path.join(directory_path, name)
        output.append(
            {
                "name": file_upload_path,
                "data": {
                    "count": len(queryset),
                    "url": url,
                    "next": next,
                    "prev": prev,
                    "results": page,
                },
            }
        )

    if len(sets) == 0:
        name = "set-1.json"
        url = os.path.join(static_path, name)
        output.append(
            {
                "name": os.path.join(directory_path, name),
                "data": {
                    "count": 0,
                    "url": url,
                    "next": None,
                    "prev": None,
                    "results": [],
                },
            }
        )

    return output


@shared_task(acks_late=True)
def bake_post_data(uuid):
    fc = FactCheck.objects.get(id=uuid)
    slug = fc.slug

    logger.info("\n\nBaking Post Data: {}...".format(slug))
    post_data = FactCheckArticleSerializer(fc).data

    name = slug + ".json"
    file_upload_path = os.path.join(S3_UPLOAD_ROOT, "api/posts", name)
    publish_to_aws(file_upload_path, post_data)


@shared_task(acks_late=True)
def unbake_post_data(uuid):
    fc = FactCheck.objects.get(id=uuid)
    slug = fc.slug

    logger.info("\n\nRemoving Post Data: {}...".format(slug))

    name = slug + ".json"
    file_upload_path = os.path.join(S3_UPLOAD_ROOT, "api/posts", name)
    remove_from_aws(file_upload_path)


@shared_task(acks_late=True)
def bake_feed_data():
    logger.info("\n\nBaking feed...")
    all_posts = FactCheck.objects.filter(status="pub").order_by(
        "-publish_date"
    )

    for datafile in paginate(all_posts, "api/feed"):
        publish_to_aws(datafile["name"], datafile["data"])


@shared_task(acks_late=True)
def bake_type_data(type):
    logger.info("\n\nBaking Type: {}...".format(type))
    all_posts = FactCheck.objects.filter(status="pub").order_by(
        "-publish_date"
    )
    filtered_posts = all_posts.filter(
        claim_reviewed__disinformation_type__label=type
    )

    for datafile in paginate(filtered_posts, "api/types/{}".format(type)):
        publish_to_aws(datafile["name"], datafile["data"])


@shared_task(acks_late=True)
def bake_tags_data(tags):
    all_posts = FactCheck.objects.filter(status="pub").order_by(
        "-publish_date"
    )

    tags = tags if isinstance(tags, list) else [tags]
    for tag in tags:
        logger.info("\n\nBaking Tag: {}...".format(tag))
        filtered_posts = all_posts.filter(claim_reviewed__tags__slug=tag)

        for datafile in paginate(filtered_posts, "api/tags/{}".format(tag)):
            publish_to_aws(datafile["name"], datafile["data"])


@shared_task(acks_late=True)
def bake_web_context():
    logger.info("\n\nBaking Web Context...")
    types = DisinformationTypeContextSerializer(
        DisinformationType.objects.all(), many=True
    )

    tags = [{"slug": tag.slug, "label": tag.name} for tag in Tag.objects.all()]

    date_modified = (
        FactCheck.objects.all()
        .filter(status="pub")
        .order_by("-date_modified")[0]
        .date_modified
    )

    context = {
        "types": types.data,
        "tags": tags,
        "date_modified": date_modified.strftime("%m/%d/%Y"),
    }

    name = "context" + ".json"
    file_upload_path = os.path.join(S3_UPLOAD_ROOT, "api", name)
    publish_to_aws(file_upload_path, context)
