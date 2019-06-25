# formatters/compositetableformatter.py

from ..tableformatter import TableFormatter

class CompositeTableFormatter(TableFormatter):
    def __init__(self):
        self.formatters = []

    def header(self, *headers):
        for formatter in self.formatters:
            formatter.header(*headers)

    def footer(self, *footer):
        for formatter in self.formatters:
            formatter.footer(*footer)

    def row(self, rowdata):
        for formatter in self.formatters:
            formatter.row(rowdata)

    def __enter__(self):
        for formatter in self.formatters:
            formatter.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        for formatter in self.formatters:
            formatter.__exit__(type, value, traceback)

    def add_formatter(self, formatter):
        '''Adds a formatter to the formatter list'''
        assert isinstance(formatter, TableFormatter)
        self.formatters.append(formatter)