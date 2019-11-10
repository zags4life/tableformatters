# table_formatters/csvtableformatter.py

from ..register_formatter import register_formatter
from ..tableformatter import TableFormatter

@register_formatter('csv')
class CSVTableFormatter(TableFormatter):
    def __init__(self, filename=None, column_widths=None, header_widths=None,
            footer_widths=None, **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self.stream = None

    def header(self, data):
        '''Writes the header to the csv file'''
        if not super().header(data):
            return

        self.__print_formatted([v.title() for v in data.header_values])

    def row(self, rowdata):
        if not super().row(rowdata):
            return

        self.__print_formatted([v for v in rowdata.row_values])

    def footer(self, *footer):
        if not super().footer(*footer):
            return

        self.__print_formatted(footer)

    def __print_formatted(self, data):
        # First ensure there are no commas in the data

        enriched_data = [str(d) if ',' not in str(d) else '"{}"'.format(d) for d in data]

        self.stream.write('{}\n'.format(','.join(enriched_data)))

    def __enter__(self):
        if self.filename:
            self.stream = open(self.filename, 'w')
        return self

    def __exit__(self, type, value, traceback):
        if self.stream:
            self.stream.close()