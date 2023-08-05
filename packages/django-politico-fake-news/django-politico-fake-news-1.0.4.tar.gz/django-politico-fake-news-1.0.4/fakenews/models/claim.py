from django.db import models
from taggit.managers import TaggableManager


class Claim(models.Model):
    """A (false) claim made by someone that we want to fact check."""

    short_text = models.CharField(
        help_text="A summary of the claim (75 character limit)",
        max_length=75,
        blank=True,
    )

    archive_url = models.URLField(
        help_text="A permanent record of the claim being made",
        max_length=500,
        blank=True,
    )
    canoncial_url = models.URLField(
        help_text="The original or most prominent spreading of the claim",
        blank=True,
    )

    disinformation_type = models.ForeignKey(
        "DisinformationType", null=True, on_delete=models.PROTECT
    )

    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.short_text
