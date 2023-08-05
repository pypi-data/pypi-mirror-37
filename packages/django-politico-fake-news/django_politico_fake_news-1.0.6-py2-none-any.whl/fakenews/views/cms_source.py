from django.views.generic.edit import CreateView, UpdateView, DeleteView

from fakenews.models import Source
from fakenews.authentication import secure
from .cms_base import CMSForm, CMSList, CMSBaseMixin, CMSBaseEditMixin


class SourceBaseMixin(object):
    url_basename = 'source'
    title = "Sources"


class SourceForm(CMSForm):
    class Meta:
        model = Source
        fields = ["name", "url", "description"]


class SourceViewMixin(SourceBaseMixin, CMSBaseEditMixin):
    form_class = SourceForm

    def get_object(self, queryset=None):
        return Source.objects.get(pk=self.kwargs['pk'])


@secure
class SourceCreate(SourceViewMixin, CreateView):
    pass


@secure
class SourceUpdate(SourceViewMixin, UpdateView):
    pass


@secure
class SourceDelete(SourceViewMixin, DeleteView):
    pass


@secure
class SourceList(SourceBaseMixin, CMSBaseMixin, CMSList):
    model = Source
    fields = ["name", "url"]


source_views = {
    "list": SourceList,
    "create": SourceCreate,
    "update": SourceUpdate,
    "delete": SourceDelete
}
