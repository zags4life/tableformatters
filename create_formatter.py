# table_formatter/create_formatter.py

import re

from .register_formatter import FORMATTER_LOOKUP
from .formatters.compositetableformatter import CompositeTableFormatter

def create_formatter(formatter, **kwargs):
    formatter = FORMATTER_LOOKUP.get(formatter.lower())
    assert formatter, "Unknown formatter type '{}'".format(formatter)
    return formatter(**kwargs)

def create_formatters(formatters, **kwargs):
    if not formatters:
        return None

    assert formatters is not None, "No formatters where specified"

    table_formatter = CompositeTableFormatter()
    for formatter in re.split(',|;|\.| ', formatters):
        table_formatter.add_formatter(create_formatter(formatter, **kwargs))
    return table_formatter
