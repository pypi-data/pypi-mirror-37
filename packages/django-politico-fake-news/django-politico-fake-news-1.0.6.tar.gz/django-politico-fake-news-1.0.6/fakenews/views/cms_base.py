from django import forms
from django.views.generic import ListView
from django.urls import reverse_lazy
from fakenews.conf import settings as app_settings


class CMSTokens(object):
    API_TOKEN = app_settings.API_TOKEN
    API_ROOT = reverse_lazy('api-root')
    POLITICO_SERVICES_ROOT = app_settings.POLITICO_SERVICES_ROOT
    POLITICO_SERVICES_TOKEN = app_settings.POLITICO_SERVICES_TOKEN

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["API_TOKEN"] = self.API_TOKEN
        context["API_ROOT"] = self.API_ROOT
        context["POLITICO_SERVICES_ROOT"] = self.POLITICO_SERVICES_ROOT
        context["POLITICO_SERVICES_TOKEN"] = self.POLITICO_SERVICES_TOKEN
        return context


class CMSForm(CMSTokens, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs.update({
                'id': self.fields[field].label,
                'class': 'form-control'
            })


class CMSList(CMSTokens, ListView):
    template_name = "fakenews/cms-base-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["fields"] = self.fields
        context["allowNew"] = True
        return context


class CMSBaseMixin(object):
    @property
    def success_url(self):
        return reverse_lazy('fakenews-cms-' + self.url_basename)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title
        context["active_page"] = self.url_basename
        context["url_base"] = 'fakenews-cms-' + self.url_basename
        context["url_update"] = context["url_base"] + "-update"
        context["url_api"] = "fakenews-{}-list".format(self.url_basename)
        return context


class CMSBaseEditMixin(CMSTokens, CMSBaseMixin):
    def __init__(self):
        self.template_name = "fakenews/cms-base-edit.html"
