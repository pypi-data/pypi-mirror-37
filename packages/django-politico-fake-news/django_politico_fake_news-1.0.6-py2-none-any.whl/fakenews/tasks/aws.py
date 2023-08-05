import logging
import json

from fakenews.utils.aws import defaults, get_bucket
from celery import shared_task

logger = logging.getLogger("tasks")


@shared_task(acks_late=True)
def publish_to_aws(filepath, data, maxage="max-age=30"):
    cache_header = str(maxage)
    bucket = get_bucket()

    bucket.put_object(
        Key=filepath,
        ACL=defaults.ACL,
        Body=json.dumps(data),
        CacheControl=cache_header,
        ContentType="application/json",
    )

    logger.info("{} published to AWS.".format(filepath))


@shared_task(acks_late=True)
def remove_from_aws(filepath):
    bucket = get_bucket()

    bucket.delete_objects(Delete={"Objects": [{"Key": filepath}]})

    logger.info("{} removed from AWS.".format(filepath))
