from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from fakenews.models import Claim, FactCheck, Share
from fakenews.authentication import TokenAPIAuthentication


class Deserializer(APIView):
    """
    View to handle data from custom Fact Check admin.
    """
    authentication_classes = (TokenAPIAuthentication,)
    permission_classes = (IsAuthenticated,)

    def parse_payload(self, payload):
        """
        Separate payload into corresponding model parts.
        """
        claim_data = payload.pop("claim_reviewed")
        share_data = claim_data.pop("share_set")
        tags_data = claim_data.pop("tags")
        fact_check_data = payload

        return claim_data, share_data, tags_data, fact_check_data

    def post(self, request, format=None):
        """
        Add a new Fact Check record.
        """
        # Parse out data
        (
            claim_data,
            share_data,
            tags_data,
            fact_check_data
        ) = self.parse_payload(request.data)

        # Create the claim record
        c = Claim(**claim_data)
        c.save()

        # Add tags to the claim
        c.tags.add(*tags_data)

        # Create the share records
        for share in share_data:
            s = Share(**share)
            s.claim = c
            s.save()

        # Create the fact check record
        fact_check_data["claim_reviewed_id"] = c.id
        fc = FactCheck(**fact_check_data)
        fc.save()

        return Response({"id": fc.id})

    def put(self, request, format=None):
        """
        Update an existing Fact Check record.
        """
        # Parse out data
        (
            claim_data,
            share_data,
            tags_data,
            fact_check_data
        ) = self.parse_payload(request.data)

        # Retrieve fact check record to be edited
        try:
            fc = FactCheck.objects.get(id=fact_check_data.pop("id"))
        except ObjectDoesNotExist:
            raise Http404()

        # Update claim record
        claim_pk = fc.claim_reviewed.pk
        c, created = Claim.objects.update_or_create(
            pk=claim_pk,
            defaults=claim_data
        )

        # Update tags
        current_tag_list = [tag.name for tag in c.tags.all()]
        added_tags = diff(tags_data, current_tag_list)
        deleted_tags = diff(current_tag_list, tags_data)
        c.tags.remove(*deleted_tags)
        c.tags.add(*added_tags)

        # Update shares
        for share in share_data:
            if share["pk"] is not None:
                Share.objects.update_or_create(pk=share["pk"], defaults=share)

        # Remove deleted shares
        current_shares = [share.pk for share in c.share_set.all()]
        kept_shares = [
            share["pk"] for share in share_data if share["pk"] is not None
        ]
        deleted_shares = diff(current_shares, kept_shares)
        Share.objects.filter(pk__in=deleted_shares).delete()

        # Create new share records
        new_shares = [share for share in share_data if share["pk"] is None]
        for share in new_shares:
            s = Share(**share)
            s.claim = c
            s.save()

        # Update fact check record
        FactCheck.objects.update_or_create(id=fc.id, defaults=fact_check_data)

        return Response(200)

    def delete(self, request, format=None):
        """
        Delete an existing Fact Check record.
        """
        try:
            fc = FactCheck.objects.get(id=request.data.pop("id"))
        except ObjectDoesNotExist:
            raise Http404()

        claim = fc.claim_reviewed
        claim.delete()

        return Response(200)


def diff(a, b):
    """
    Returns the relative complement (A\B)
    (i.e. everything in A that is NOT in B)
    """
    return [tag for tag in a if tag not in b]
