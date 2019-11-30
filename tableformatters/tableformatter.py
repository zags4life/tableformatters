# table_formatters/table_formatter.py

from abc import (
    ABC,
    abstractproperty,
    abstractmethod
)
import logging
import re

from .tabledataprovider import TableFormatterDataProvider
from .utils.column_width import ColumnWidth
from .utils.display_options import DisplayOptions

logger = logging.getLogger(__name__)

class TableFormatter(ABC):
    '''Abstract base class for all table formatters

    Parameters:
        column_widths: a list or tuple of strings defining the column widths
            using the Column Width Mini-Language
        header_widths: a list or tuple of strings defining the column widths
            using the Column Width Mini Language.  This parameter is optional.
            If this parameter is not specified, the same column widths will be
            used for both headers and rows, as specified in column_widths.
        display_options: a delimitated string, specifying the display options.
            This parameter is optional where the default is 'headers;footers;rows'

            This is intended for use with CompositeTableFormatter where each
            formatter needs to display different content, thus allowing the
            user to display everything and rely on the table formatter to
            display the correct content

            example:
                'headers;footers'
                'headers,rows;footers'
    '''
    def __init__(self, column_widths=None, header_widths=None, footer_widths=None,
            display_options='headers;footers;rows', **kwargs):

        self.column_widths = column_widths
        self.header_widths = header_widths
        self.footer_widths = footer_widths

        if self.column_widths:
            self.column_widths = [ColumnWidth(cw) for cw in self.column_widths]

        if self.header_widths:
            self.header_widths = [ColumnWidth(cw) for cw in self.header_widths]
        else:
            self.header_widths = self.column_widths

        if self.footer_widths:
            self.footer_widths = [ColumnWidth(cw) for cw in self.footer_widths]
        else:
            self.footer_widths = self.column_widths

        self.display_options = []
        for option in re.split(',|;|\.| ', display_options.lower()):
            self.display_options.append(DisplayOptions(option))

    @abstractmethod
    def header(self, data):
        assert isinstance(data, TableFormatterDataProvider), \
            '{} is not enabled for formatting.  Please ensure it is a ' \
            'TableFormatterDataProvider.'.format(data.__class__.__name__)

        if self.column_widths and len(data.row_values) > len(self.column_widths):
            logger.warning('Column width / row data mismatch - the number of ' \
                'column_widths does not match the number of row entries. ' \
                'This may result in some row data not being displayed' \
                'Column Widths: {}, Row Data: {}'.format(
                    len(self.column_widths),
                    len(data.row_values)
                )
            )

        return DisplayOptions.Headers in self.display_options

    @abstractmethod
    def footer(self, *values):
        return DisplayOptions.Footers in self.display_options

    @abstractmethod
    def row(self, data):
        assert isinstance(data, TableFormatterDataProvider), \
            '{} is not enabled for formatter.  Please ensure it is a ' \
            'TableFormatterDataProvider.'.format(data.__class__.__name__)

        return DisplayOptions.Rows in self.display_options

    def writelines(self, dataset):
        '''A generator method that writes lines for a given dataset'''
        if not dataset:
            return

        for idx, data in enumerate(dataset):
            # If it is the first, display headers
            if idx == 0:
                self.header(data)

            # Display row
            self.row(data)

            # Yield to the caller
            yield data


    ##########################################################
    # with statement support implementation
    ##########################################################
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    ##########################################################
    # helper methods
    ##########################################################
    @classmethod
    def _format_msg(self, dataset, column_widths, resize=True):
        if not column_widths:
            return [str(d) for d in dataset]

        return [cw.format(d, resize) for cw, d in zip(column_widths, dataset)]


class StringTableFormatter(TableFormatter):
    @abstractproperty
    def output(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    def __str__(self):
        return self.output