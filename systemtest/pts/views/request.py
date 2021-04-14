# Python
from typing import Any

# Django Forms
from django.forms.forms import BaseForm
from django.forms.formsets import formset_factory

# Django HTTP
from django.urls.base import reverse_lazy
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect

# Django Views
from django.views.generic import FormView

# Django Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

# APP PTS
from systemtest.pts import forms as pts_forms, models as pts_models


class RequestView(LoginRequiredMixin, FormView):
    template_name = "pts/request.html"
    success_url = reverse_lazy("pts:open")
    form_class = pts_forms.RequestGroupForm

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user_groups = self.request.user.groups.all()
        if user_groups.filter(name="TA"):
            return super().get(request, *args, **kwargs)
        elif user_groups.filter(name="IPIC NCM"):
            return HttpResponseRedirect(reverse_lazy("pts:return"))
        return HttpResponseRedirect(reverse_lazy("pts:open"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if "detailed_form" not in kwargs:
            kwargs["detailed_form"] = self.get_detailed_form()
        return super().get_context_data(**kwargs)

    def get_detailed_form(self) -> Any:
        data = self.request.POST
        parts_qty = int(data.get("qty", 1))
        are_more_fields_required = (
            parts_qty > 1 and
            data.get("is_serialized") and
            not data.get("is_vpd")
        )
        parts_qty = parts_qty if are_more_fields_required else 1

        formset = formset_factory(
            pts_forms.RequestPartForm,
            formset=pts_forms.RequestPartFormset,
            extra=parts_qty,
        )
        return formset

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = self.get_form()
        if form.is_valid() and request.POST.get("form-0-part_id"):
            detailed_form = self.get_detailed_form()(form.data)
            if detailed_form.is_valid():
                return self.form_valid(form, detailed_form)

            return self.form_invalid(detailed_form=detailed_form)

        return self.form_invalid(form=form)

    def form_valid(self, form, *args) -> HttpResponse:
        data = form.cleaned_data

        request_group = form.save(commit=False)
        user = self.request.user

        detailed_form = args[0]
        part_id_set = detailed_form.cleaned_data

        part_number = part_id_set[0].get("pn")
        request_group.part_number = part_number

        request_group.save()
        if data.get("is_serialized"):
            for part_id in part_id_set:
                request = pts_models.Request(
                    request_group=request_group,
                    part_number=part_number,
                    serial_number=part_id.get("sn"),
                    user=user
                )
                request.save()
        else:
            for _ in range(data.get("qty")):
                request = pts_models.Request(
                    request_group=request_group,
                    part_number=part_number,
                    user=user
                )
                request.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, **kwargs) -> HttpResponse:
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(**kwargs))
