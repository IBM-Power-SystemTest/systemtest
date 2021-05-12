"""
Utilities for Django Models
"""

from typing import Any


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
