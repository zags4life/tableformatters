# utils/column_width.py

import logging
import re

logger = logging.getLogger(__name__)

COLUMN_WIDTH_REGEX = re.compile(
                        r'(?P<prefix>^\D*?)' \
                            '(?P<width>\d+)' \
                            '(?P<precision>[,.\d]*?)' \
                            '(?P<type>((b|c|d|e|E|f|F|g|G|n|o|s|x|X|%){1})?)'
                            '(?P<alignment>(<|\^|>|=))' \
                            '(?P<suffix>.*$)',
                        re.VERBOSE)

class ColumnWidth(object):
    '''Specifies the width of a column

    Parameters:
        column_width: A string representing the column width using the
            Column Width Mini-Language.
    '''
    def __init__(self, column_width):
        self.width = ''
        self.alignment = ''
        self.prefix = ''
        self.suffix = ''
        self.precision = ''

        self.__parse(column_width)

    def __parse(self, column_width):
        # Expected string format '<prefix><width><precision><type><alignment><suffix>'
        assert column_width and isinstance(column_width, str), \
            'column_width cannot be None and must be a string'

        parsed_values = COLUMN_WIDTH_REGEX.match(column_width)

        if not parsed_values:
            logger.error("Failed to parse column_width '{}'".format(column_width))
            return

        self.prefix = parsed_values['prefix']
        self.suffix = parsed_values['suffix']
        self.alignment = parsed_values['alignment']
        self.precision = parsed_values['precision'] + parsed_values['type']

        self.width = int(parsed_values['width'])
        self.width -= len(self.prefix)

    def __str__(self):
        return "Prefix='{0.prefix}', Width={0.width}, Precision={0.precision}, Alignment={0.alignment}, " \
            " Suffix='{0.suffix}'".format(self)

    def __repr__(self):
        return 'ColumnWidth({})'.format(str(self))

    def format(self, data, resize=True):
        '''Formats the data based on the column width

        Parameters:
            data: the data to format
            resize: a boolean indicating whether to resize the data to fit the
                column width.  If True, the data will be truncated to the width
                of the column; if False the data can overrun the column width
                but will guarantee the data in its entirety is output.

        Returns: A formatted string
        '''
        # format data using precision
        formatted_data = '{1:{0.precision}}'.format(self, data)

        # If resize, truncate the message to fit width
        if resize:
            formatted_data = formatted_data[:self.width]

        # Append suffix
        formatted_data = '{1}{0.suffix}'.format(self, formatted_data)

        # Format the data using alignment and width
        if not resize:
            formatted_data = '{1:{0.alignment}}'.format(self, formatted_data)
        else:
            formatted_data = '{1:{0.alignment}{0.width}}'.format(self, formatted_data)

        # Prepend prefix
        formatted_data = '{0.prefix}{1}'.format(self, formatted_data)

        return formatted_data

if __name__ == '__main__':

    s = '$12,.2f>#'
    print(s)
    c = ColumnWidth(s)

    print(c)