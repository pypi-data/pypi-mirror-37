"""
Use this file to configure pluggable app settings and resolve defaults
with any overrides set in project settings.
"""

from django.conf import settings as project_settings

from fakenews.utils.importers import import_class


class Settings:
    pass


Settings.AUTH_DECORATOR = import_class(
    getattr(
        project_settings,
        "FAKENEWS_AUTH_DECORATOR",
        "django.contrib.auth.decorators.login_required",
    )
)

Settings.SECRET_KEY = getattr(
    project_settings, "FAKENEWS_SECRET_KEY", "a-bad-secret-key"
)

Settings.AWS_ACCESS_KEY_ID = getattr(
    project_settings, "FAKENEWS_AWS_ACCESS_KEY_ID", None
)

Settings.AWS_SECRET_ACCESS_KEY = getattr(
    project_settings, "FAKENEWS_AWS_SECRET_ACCESS_KEY", None
)

Settings.AWS_REGION = getattr(project_settings, "FAKENEWS_AWS_REGION", None)

Settings.AWS_S3_BUCKET = getattr(
    project_settings, "FAKENEWS_AWS_S3_BUCKET", None
)

Settings.CLOUDFRONT_ALTERNATE_DOMAIN = getattr(
    project_settings, "FAKENEWS_CLOUDFRONT_ALTERNATE_DOMAIN", None
)

Settings.S3_UPLOAD_ROOT = getattr(
    project_settings, "FAKENEWS_S3_UPLOAD_ROOT", "uploads/fakenews"
)

Settings.S3_STATIC_ROOT = getattr(
    project_settings, "FAKENEWS_S3_STATIC_ROOT", "https://www.politico.com"
)

Settings.API_TOKEN = getattr(project_settings, "FAKENEWS_API_TOKEN", "")

Settings.POLITICO_SERVICES_TOKEN = getattr(
    project_settings, "FAKENEWS_POLITICO_SERVICES_TOKEN", ""
)

Settings.POLITICO_SERVICES_ROOT = getattr(
    project_settings,
    "FAKENEWS_POLITICO_SERVICES_ROOT",
    "https://staging.politicoapps.com/api/services/",
)

Settings.STATICS_HASH = getattr(
    project_settings, "FAKENEWS_STATICS_HASH", "hdiT8FzsAX"
)


settings = Settings
