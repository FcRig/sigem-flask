
def strip_strings(obj):
    """Recursively strip whitespace from all string values."""
    if isinstance(obj, str):
        return obj.strip()
    if isinstance(obj, dict):
        return {k: strip_strings(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_strings(v) for v in obj]
    return obj

