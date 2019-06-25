# table_formatters/consoletableformatter.py

import sys

from ..register_formatter import register_formatter
from ..tableformatter import TableFormatter

TABLE_PADDING = '  '

@register_formatter('stream')
@register_formatter('console')
class StreamTableFormatter(TableFormatter):
    '''A TableFormatter the prints a table to the console

    See TableFormatter documentation for more information

        import table_formatters

        help(table_formatters.TableFormatter)
    '''

    def __init__(self, output_stream=sys.stdout, **kwargs):
        super().__init__(**kwargs)

        self.__stream = output_stream
        self.__msg_length = None
        
    def header(self, data):
        '''Displays the header to the console'''
        if not super().header(data):
            return

        self.__stream.write('\n')
        self.__print_formatted(data.header_values, self.header_widths)

    def footer(self, *values):
        '''Prints the footer to the console'''
        if not super().footer(*values):
            return

        # Display border
        self.__stream.write('_' * self.__msg_length + '\n')

        # Display footer
        self.__print_formatted(values, self.column_widths)
        self.__stream.write('\n')

    def row(self, rowdata):
        '''Prints a single row to the console'''

        # Call the base call to ensure 'rows' are defined in the
        # display options.  Is the base class returns None, stop.
        if not super().row(rowdata):
            return

        # Print the row values
        self.__print_formatted(rowdata.row_values, self.column_widths)

    def __print_formatted(self, data, column_widths):
        '''Prints the data to the console'''
        # Format the msg using the provided column widths
        msg = TABLE_PADDING.join(
            self._format_msg(
                dataset=data,
                column_widths=column_widths
            )
        )

        # If the message length is not set, set the  message length to the
        # the current msg
        if not self.__msg_length:
            self.__msg_length = len(msg)

        # Write the message to the output stream
        self.__stream.write(msg + '\n')