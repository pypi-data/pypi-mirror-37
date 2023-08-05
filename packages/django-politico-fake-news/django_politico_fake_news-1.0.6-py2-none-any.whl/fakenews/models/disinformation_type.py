from django.db import models


class DisinformationType(models.Model):
    """A type of disinformation (e.g. Hoax, Photoshopped Image)."""
    label = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    color_primary = models.CharField(max_length=30, blank=True)
    color_light = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.label
