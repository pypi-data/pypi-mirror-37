import os
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from fakenews.models import FactCheck
from fakenews.authentication import secure
from fakenews.conf import settings
from fakenews.serializers import FactCheckArticleSerializer
from .web_base import WebBaseView
from .meta import meta


class WebArticle(WebBaseView):
    name = "fakenews-web-article"
    path = "(?P<slug>)"

    js_dev_path = "fakenews/js/main-web.js"
    css_dev_path = "fakenews/css/main-web.css"

    model = FactCheck
    context_object_name = "package"
    template_name = "fakenews/web-article.html"

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, **kwargs):
        return get_object_or_404(self.model, slug=self.kwargs.get("slug"))

    def get_publish_path(self):
        return "interactives/2018/is-this-true/{}".format(self.slug)

    def get_serialized_data(self):
        package = self.get_object()
        return FactCheckArticleSerializer(package).data

    def get_metadata(self, **kwargs):
        global_metadata = super().get_context_data(**kwargs)

        data = self.get_serialized_data()

        page_metadata = {
            "publishPath": self.get_publish_path() + "/",
            "timestamp": data["publish_date"],
            "dateline": data["publish_date"],
            "share": {
                "fbook": {
                    "card_title": data["headline"],
                    "card_description": data["deck"],
                    "author": "politico",
                },
                "twitter": {
                    "card_title": data["headline"],
                    "card_description": data["deck"],
                    "author": "@politico",
                },
                "image": meta["share"]["image"],
                "keywords": " ".join(data["claim_reviewed"]["tags"]),
            },
        }

        return {**global_metadata, **page_metadata}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.slug = self.kwargs.get("slug")

        context["secret"] = settings.SECRET_KEY
        context["ARTICLE_SLUG"] = self.kwargs["slug"]
        context["data"] = self.get_serialized_data()
        context["meta"] = self.get_metadata()
        context["API_ROOT"] = os.path.join(
            settings.S3_STATIC_ROOT, settings.S3_UPLOAD_ROOT
        )

        return {
            **context,
            **self.get_paths_context(production=context["production"]),
        }
