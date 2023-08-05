from django.db import models
from django.template.defaultfilters import slugify


class Source(models.Model):
    """A source of disinformation."""
    name = models.CharField(max_length=50, blank=True)
    url = models.URLField()

    description = models.TextField(
        help_text="A Wikipedia-like description of the source",
        blank=True
    )

    def __str__(self):
        return self.name
