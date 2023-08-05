import logging
from celery import shared_task
from fakenews.views import WebArticle

logger = logging.getLogger("tasks")


@shared_task(acks_late=True)
def bake_post_template(slug):
    kwargs = {"slug": slug}
    view = WebArticle(**kwargs)

    logger.info("\n\nBaking Post Template: {}...".format(slug))
    view.publish_template(**kwargs)


@shared_task(acks_late=True)
def unbake_post_template(slug):
    kwargs = {"slug": slug}
    view = WebArticle(**kwargs)

    logger.info("\n\nRemoving Post Template: {}...".format(slug))
    view.unpublish_template(**kwargs)
