from django.db import models


class Share(models.Model):
    """An instance of a Claim shared by a Source."""
    url = models.URLField(
        help_text="The canoncial link to a source spreading a claim."
    )
    publish_date = models.DateField(
        help_text="The date this claim was spread by this source.",
        null=True
    )

    order = models.IntegerField(default=0, null=False)

    claim = models.ForeignKey('Claim', on_delete=models.CASCADE)
    source = models.ForeignKey('Source', on_delete=models.PROTECT)

    def __str__(self):
        return '%s: %s' % (self.source.name, self.claim.text)

    class Meta:
        ordering = ('order',)
