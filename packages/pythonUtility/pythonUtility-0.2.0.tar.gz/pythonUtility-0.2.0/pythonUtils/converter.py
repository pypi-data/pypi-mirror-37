import re


def to_int(param, **kwargs):
    return base_converter(param, _default_regex="(\d+)", _base_converter=int, **kwargs)


def to_float(param, **kwargs):

    def float_converer(p):
        if isinstance(p, (tuple, list)):
            return float(p[0])
        return float(p)

    return base_converter(param, _default_regex="(\d+(\.\d+|))", _base_converter=float_converer,  **kwargs)


def base_converter(param, _default_regex, _base_converter,
                   default=0.0, exception=(ValueError, TypeError,), regex=None, match_group_index=-1):
    if regex is True:
        regex = _default_regex

    if isinstance(regex, str):
        regex = re.compile(regex)
    elif hasattr(regex, "findall"):
        pass
    elif regex is not None:
        raise TypeError("Unknown argument for regex match: %r".format(regex))

    try:
        if regex:
            match = regex.findall(param)
            if match:
                param = match[match_group_index]

        return _base_converter(param)
    except exception:
        param = default

    return default
