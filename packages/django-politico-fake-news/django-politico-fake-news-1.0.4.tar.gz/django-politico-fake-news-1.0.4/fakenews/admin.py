from django.contrib import admin

from .models import (
    DisinformationType,
    Claim,
    FactCheck,
    Source,
    Share,
)


class ClaimAdmin(admin.ModelAdmin):
    fields = (
        'short_text',
        'archive_url',
        'canoncial_url',
        'disinformation_type'
    )


admin.site.register(DisinformationType)
admin.site.register(Claim, ClaimAdmin)
admin.site.register(FactCheck)
admin.site.register(Source)
admin.site.register(Share)
