

from typing import Any


def set_placeholder(field: Any, text: str) -> Any:
    field.widget.attrs["placeholder"] = text
    return field
