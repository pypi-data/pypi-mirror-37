import re
import math
from django.db.models import Q
from django.views import View
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, reverse

from fakenews.models import FactCheck, DisinformationType
from django.contrib.auth.models import User
from fakenews.authentication import secure
from .cms_base import CMSTokens


@secure
class CMSPackageHome(View):
    def get(self, request, *args, **kwargs):
        return redirect(reverse('fakenews-cms-page', kwargs={"page": "1"}))


@secure
class CMSPackageList(CMSTokens, ListView):
    template_name = "fakenews/cms-package-list.html"
    model = FactCheck
    artices_per_page = 50

    def get_queryset(self):
        self.filters = {}
        object_list = self.model.objects.all().select_related(
            'claim_reviewed',
            'claim_reviewed__disinformation_type',
            'author'
        ).prefetch_related('claim_reviewed__tags')

        # Inclusive Search Function
        search = self.request.GET.get("search", "")
        if (search != ""):
            object_list = object_list.filter(
                Q(headline__icontains=search) |
                Q(deck__icontains=search) |
                Q(claim_reviewed__short_text__icontains=search) |
                Q(claim_reviewed__tags__name__in=search.split(" "))
            )
        self.filters["search"] = search

        # Filter Author First Name
        author_first = self.request.GET.get("fname", "")
        author_first_parts = re.split(r'\s+|\|', author_first)
        if (author_first != ""):
            object_list = object_list.filter(
                author__first_name__in=author_first_parts
            )
        self.filters["author_firsts"] = author_first_parts

        # Filter Author Last Name
        author_last = self.request.GET.get("lname", "")
        author_last_parts = re.split(r'\s+|\|', author_last)
        if (author_last != ""):
            object_list = object_list.filter(
                author__last_name__in=author_last_parts
            )
        self.filters["author_lasts"] = author_last_parts

        # Filter Type
        type = self.request.GET.get("type", "")
        types = type.split("|")
        if (type != ""):
            object_list = object_list.filter(
                claim_reviewed__disinformation_type__label__in=types
            )
        self.filters["type"] = types

        # Filter Status
        status = self.request.GET.get("status", "")
        statuses = status.split("|")
        if (status != ""):
            object_list = object_list.filter(
                status__in=statuses
            )
        self.filters["status"] = statuses

        # Filter Tags
        tag = self.request.GET.get("tag", "")
        tags = tag.split("|")
        if (tag != ""):
            object_list = object_list.filter(
                claim_reviewed__tags__name__in=tags
            )

        # Remove duplicates and order by date published and date_modified
        object_list = object_list.distinct().order_by(
            "status", "-publish_date", "-date_modified"
        )

        # Handle pagination
        self.page = int(self.kwargs["page"]) if "page" in self.kwargs else 1
        self.pages = math.ceil(len(object_list)/self.artices_per_page)
        limit = (self.page-1) * self.artices_per_page
        offset = self.page * self.artices_per_page
        object_list = object_list[limit:offset]

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search"] = self.filters["search"]

        context["types"] = [
            {
                "label": str(label),
                "active": str(label) in self.filters["type"]
            }
            for label in DisinformationType.objects.all()
        ]

        context["statuses"] = [
            {
                "slug": status[0],
                "label": status[1],
                "active": status[0] in self.filters["status"]
            }
            for status in FactCheck.STATUS_TYPES
        ]
        context["statusTypes"] = {}
        for status in FactCheck.STATUS_TYPES:
            context["statusTypes"][status[0]] = status[1]

        context["authors"] = [
            {
                "label": "{} {}".format(author.first_name, author.last_name),
                "pk": author.pk,
                "first": author.first_name,
                "last": author.last_name,
                "active": (
                    author.first_name in self.filters["author_firsts"]
                    and author.last_name in self.filters["author_lasts"]
                )
            }
            for author in (
                User.objects.filter(factcheck__isnull=False).distinct()
            )
        ]

        context["page"] = self.page
        context["pages"] = range(1, self.pages+1)

        return context


@secure
class CMSPackageNew(CMSTokens, TemplateView):
    template_name = "fakenews/cms-package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "new_article"
        context["api_deserializer"] = reverse('fakenews-cms-deserializer')
        return context


@secure
class CMSPackageEdit(CMSTokens, TemplateView):
    template_name = "fakenews/cms-package.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["slug"] = self.kwargs["slug"]
        return context


package_views = {
    "home": CMSPackageHome,
    "list": CMSPackageList,
    "create": CMSPackageNew,
    "update": CMSPackageEdit
}
