# formatters/nonetableformatter.py

from ..register_formatter import register_formatter
from ..tableformatter import TableFormatter

@register_formatter('none')
class NoneTableFormatter(TableFormatter):
    def header(self, data):
        pass

    def footer(self, *values):
        pass

    def row(self, data):
        pass