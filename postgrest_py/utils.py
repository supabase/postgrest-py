def sanitize_param(param: str) -> str:
    reserved_chars = ",.:()"
    if any(char in param for char in reserved_chars):
        return f'"{param}"'
    return param


def sanitize_pattern_param(pattern: str) -> str:
    return sanitize_param(pattern.replace("%", "*"))
