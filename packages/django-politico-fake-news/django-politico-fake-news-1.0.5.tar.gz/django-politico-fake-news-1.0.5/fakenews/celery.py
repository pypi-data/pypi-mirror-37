# flake8: noqa
from fakenews.tasks.aws import publish_to_aws
from fakenews.tasks.data_bakery import (
    bake_post_data,
    bake_feed_data,
    bake_type_data,
    bake_tags_data,
    unbake_post_data,
    bake_web_context,
)
from fakenews.tasks.template_bakery import (
    bake_post_template,
    unbake_post_template,
)
