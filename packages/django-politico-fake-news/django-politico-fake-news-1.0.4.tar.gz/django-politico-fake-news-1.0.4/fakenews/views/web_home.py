import os
from django.views.generic import TemplateView
from fakenews.authentication import secure
from fakenews.conf import settings

from .web_base import WebBaseView


class WebHome(WebBaseView):
    name = "fakenews-web-home"
    path = ""

    js_dev_path = "fakenews/js/main-web.js"
    css_dev_path = "fakenews/css/main-web.css"

    template_name = "fakenews/web-home.html"

    def get_queryset(self):
        pass

    def get_object(self, **kwargs):
        pass

    def get_publish_path(self):
        return "interactives/2018/is-this-true"

    def get_serialized_data(self):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["secret"] = settings.SECRET_KEY
        context["API_ROOT"] = os.path.join(
            settings.S3_STATIC_ROOT, settings.S3_UPLOAD_ROOT
        )
        context["meta"] = self.get_metadata()

        return {
            **context,
            **self.get_paths_context(production=context["production"]),
        }
