''' table_formatters/__init__.py

The Table Formatter module is designed to format generic data into a table format.

The module is made up of two parts: TableFormatters and
TableFormatterDataProvider.

A TableFormatter object is an ABC class that defines how to write headers,
rows, and footers to various output streams.  TableFormatter objects require
that all data objects passed to it inherit from TableFormatterDataProvider.

A TableFormatterDataProvider is an ABC which defines the data to be formatted
by the TableFormatter.

Example:

Imagine we have created a class that represents metadata about a person.
Now we would like to display the list of Person objects using table formatters.
This can be broken into two parts: the formatter and the data provider.

TableFormatterDataProvider:

The following example illustrates how to implement a table formatter data provider.

    from table_formatters import TableFormatterDataProvider

    class Person(TableFormatterDataProvider):
        def __init__(self, name, address, phone_number):
            self.name = name
            self.address = address
            self.phone_number = phone_number

        @property
        def row_values(self):
            # Returns a list of data to display.
            # Note: order of the list is important
            return [self.name, self.address, self.phone_number]

        @property
        def header_values(self):
            # Returns a list of strings, used as the table headers
            # Note: order of the list is important
            return ['Name', 'Address', 'Phone Number']


Table Formatter:

The following example illustrates  how to implement a custom TableFormatter
that will output the table using the python logger.

    from formatters import TableFormatter, register_formatter

    @register_formatter('logger') 
    class LoggerTableFormatter(TableFormatter):
        def __init__(self, logger, **kwargs):
            super().__init__(**kwargs)
            self._logger = logger

        def header(self, data):
            self._logger.debug(' '.join(self._format_msg(data.header_values, self.header_width)))

        def row(self, data):
            self._logger.debug(' '.join(self._format_msg(data.row_values, self.column_width)))

        def footer(self, *values):
            self._logger.debug(' '.join(self._format_msg(values, self.column_width)))


Putting It All Together:

    # Create a list of Person objects
    persons = [
        Person('Travis', 'Fake St', '555-1212'),
        Person('Tom', 'Surf St', '867-5309'),
        Person('Mike', 'Newport Ave', '879-2196'),
        Person('Kate', 'Some Where in the world', '??????'),
    ]

    # Create the formatter
    formatter = create_formatter(
        formatter_type='logger',
        column_widths=('12<', '50<', '15<')
    )

    # Write the data using the formatter
    for data in formatter.writelines(persons):
        pass

    --- or ---

    for idx, person in enumerate(person):
        if idx == 0:
            formatter.header(person)
        formatter.row(person)
    formatter.footer('footer col 1, 'footer col 2', 'footer col 3')


Column Width Mini-Language
    Column widths are defined as strings in the format
        '<prefix><padding><alignment><suffix>'

    prefix: The value to prefix to each message
    padding: The width of the column in Format Specification Mini-Language.
        https://docs.python.org/3/library/string.html#formatspec

        Examples:
            width=12
            -- or --
            width='11,.2f'
    alignment: Specifies the column alignment.
        See Formating Specification Mini-Language for more information
            https://docs.python.org/3/library/string.html#formatspec

        | Option | Meaning                                                |
        |   '<'  | Forces the field to be left-aligned within the         |
        |        | available space (this is the default for most objects) |
        |   '>'  | Forces the field to be right-aligned within the        |
        |        | available space (this is the default for numbers).     |
        |   '='  | Forces the padding to be placed after the sign (if any)|
        |        | but before the digits. This is used for printing       |
        |        | fields in the form ‘+000000120’. This alignment option |
        |        | is only valid for numeric types. It becomes the default|
        |        | when ‘0’ immediately precedes the field width.         |
        |   '^'  | Forces the field to be centered within the available   |
        |        | space.                                                 |
    suffix: The value to append to the message
'''



# Table Formatter Classes
from .formatters.streamtableformatter import StreamTableFormatter
from .formatters.csvtableformatter import CSVTableFormatter
from .formatters.loggingtableformatter import LoggerTableFormatter
from .formatters.htmltableformatter import HtmlTableFormatter
from .formatters.nonetableformatter import NoneTableFormatter

# Utility Classes
from .register_formatter import register_formatter, get_formatter_names
from .create_formatter import create_formatter, create_formatters
from .tabledataprovider import TableFormatterDataProvider
from .tableformatter import TableFormatter
