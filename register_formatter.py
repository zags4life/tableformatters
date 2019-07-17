# table_formatter/register_formatter.py

import logging

logger = logging.getLogger(__name__)

FORMATTER_LOOKUP = {}

def register_formatter(name):
    def decorator(func):
        if name in FORMATTER_LOOKUP:
            logger.warning("Formatter type '{}' has already been " \
                "registered".format(name))
        FORMATTER_LOOKUP[name] = func
        return func
    return decorator
    
def get_formatter_names():
    return sorted(list(FORMATTER_LOOKUP.keys()))
