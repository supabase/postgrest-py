from __future__ import annotations

from typing import Any

def sanitize_param(param: Any) -> str:
    param_str = str(param)
    reserved_chars = ",:()"
    if any(char in param_str for char in reserved_chars):
        return f'"{param_str}"'
    return param_str


def sanitize_pattern_param(pattern: str) -> str:
    return sanitize_param(pattern.replace("%", "*"))
