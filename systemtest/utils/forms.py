"""
Utilities for Django Models
"""
# Python
from typing import Any

# Django
from django.forms.widgets import ChoiceWidget
from django import forms

# Django filters
import django_filters as filters

def set_placeholder(field: Any, text: str) -> Any:
    """
    Pass a Django form field and set a placeholder widget attribute,
    HTML Input with placeholder attribute with value as text passed

    Args:
        field:
            Django form field (usually a CharField),
            this need to be compatible with HTML placeholder attribute.
        text:
            Text to set in placeholder

    Returns:
        The same field with the placehorder attr assigned
    """

    field.widget.attrs["placeholder"] = text
    return field


class PaginationForm(forms.Form):
    pagination_choices = (
        (10, "10"),
        (25, "25"),
        (50, "50"),
        (100, "100"),
        (150, "150"),
    )

    pagination = forms.ChoiceField(
        label="Paginate by",
        choices=pagination_choices,
        widget=forms.Select(
            attrs={
                "onchange": "this.form.submit()"
            }
        )
    )


class NumberInFilter(filters.BaseInFilter, filters.CharFilter):
    pass
