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
        if not self.request.user.groups.filter(name="TA"):
            return HttpResponseRedirect(reverse_lazy("pts:open"))

        return super().get(request, *args, **kwargs)

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

        RequestPartFormset = formset_factory(
            pts_forms.RequestPartForm,
            extra=parts_qty,
        )
        return RequestPartFormset

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

        detailed_form = args[0]

        request_group = form.save(commit=False)
        user = self.request.user

        part_id_set = detailed_form.cleaned_data
        part_number_set = {part_id.get("pn") for part_id in part_id_set} - {None}
        serial_number_set = {part_id.get("sn") for part_id in part_id_set} - {None}

        if len(part_number_set) > 1:
            error_message = "Se estan requiriendo distintos numeros de parte"
            form.add_error("part_id", error_message)
            self.form_invalid(form=form)

        part_number = part_number_set.pop()
        request_group.part_number = part_number
        request_group.save()
        if data.get("is_serialized"):
            real_qty = 0
            for serial_number in serial_number_set:
                request = pts_models.Request(
                    request_group=request_group,
                    part_number=part_number,
                    serial_number=serial_number,
                    user=user
                )
                request.save()
                real_qty += 1

            request_group.qty = real_qty
        else:
            for _ in range(data.get("qty")):
                request = pts_models.Request(
                    request_group=request_group,
                    part_number=part_number,
                    user=user
                )
                request.save()

        request_group.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, **kwargs) -> HttpResponse:
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(**kwargs))
