def is_none_or_blank(obj):
    return obj is None or (hasattr(obj, '__len__') and len(obj) == 0)


def not_none_or_blank(obj):
    return not is_none_or_blank(obj)
