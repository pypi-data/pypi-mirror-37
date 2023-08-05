from django.views.generic.edit import CreateView, UpdateView, DeleteView

from fakenews.models import DisinformationType
from fakenews.authentication import secure
from .cms_base import CMSForm, CMSList, CMSBaseMixin, CMSBaseEditMixin


class DisinformationTypeBaseMixin(object):
    url_basename = 'disinformation_type'
    title = "Types"


class DisinformationTypeForm(CMSForm):
    class Meta:
        model = DisinformationType
        fields = ["label", "description"]


class DisinformationTypeViewMixin(
    DisinformationTypeBaseMixin,
    CMSBaseEditMixin
):
    form_class = DisinformationTypeForm

    def get_object(self, queryset=None):
        return DisinformationType.objects.get(pk=self.kwargs['pk'])


@secure
class DisinformationTypeCreate(DisinformationTypeViewMixin, CreateView):
    pass


@secure
class DisinformationTypeUpdate(DisinformationTypeViewMixin, UpdateView):
    pass


@secure
class DisinformationTypeDelete(DisinformationTypeViewMixin, DeleteView):
    pass


@secure
class DisinformationTypeList(
    DisinformationTypeBaseMixin,
    CMSBaseMixin,
    CMSList
):
    model = DisinformationType
    fields = ["label", "description"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allowNew"] = False
        return context


disinformation_type_views = {
    "list": DisinformationTypeList,
    "create": DisinformationTypeCreate,
    "update": DisinformationTypeUpdate,
    "delete": DisinformationTypeDelete
}
