import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class FactCheck(models.Model):
    """A rating/explanation on how & why a claim is false."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    headline = models.CharField(
            help_text="A headline for the story (255 character limit)",
            max_length=255,
            blank=True
    )

    deck = models.TextField(blank=True)

    slug = models.SlugField(unique=True)

    explanation = JSONField(
        blank=True,
        null=True
    )

    cover = models.URLField(
        help_text="An image link to use as the cover and for social.",
        blank=True,
        null=True
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    claim_reviewed = models.ForeignKey(
        'Claim',
        on_delete=models.CASCADE
    )

    is_pinned = models.BooleanField(default=False)

    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateField(
        help_text="The date this fact check was published.",
        blank=True,
        null=True,
    )

    STATUS_TYPES = (
        ('dft', 'Draft'),
        ('fil', 'Filed'),
        ('pub', 'Published'),
    )
    status = models.CharField(
        max_length=3,
        choices=STATUS_TYPES,
        default='dft',
    )

    def __str__(self):
        return self.headline
