Table Formatters
===

## Overview
The Table Formatter module is designed to format generic data into a table format.

The module is made up of two parts: `TableFormatter` and `TableFormatterDataProvider`.

The module also include several common table formatters.  In the most general case, a consumer would be required to implement the `TableFormatterDataProvider` ABC, then output the data, as a table, using a built-in table formatter.

It is also possible to define your own `TableFormatter` in the case where a built-in formatter does not meet your needs.

## Creating a formatter
To create a `TableFormatter` object, use the factory method `create_formatter`.  `create_formatter` requires, at a minimum, a string representing the formatter you with to use.  You may also wish to specify column formatting.  This is enabled via the `column_widths` parameter, which is expected to be a tuple (or list) of strings specifying each column formatting using [Column Width Mini-Language](#Column-Width-Mini-Language).

### Built-in formatters

| Formatter | Description |
| ---- | ----------- |
| console \| stream | outputs a table to a stream.  By default, it will output to `stdout`|
| csv | outputs a table to a csv file |
| html | creates an HTML table and outputs to a string |
| logging \| logger | outputs a table to the python logger |

### Composite formatters
In a lot of cases, the user may wish to output a table to multiple outputs.  In this case, you can create a composite formatter using the `create_formatters` API.  Like `create_formatter`, the first parameter is a string representing the formatters you wish to use.

The example below illustrates creating a composite formatter that will output to the console and the python logger.  Note, the `logger` instance and `log_level` are passed to `create_formatters` as keyword arguments.

```
import logging
logger = logging.getLogger(__name__)

formatter = create_formatters(
    formatters='console;logger',
    logger=logger,
    log_level='debug'
    column_widths=('10<', '50<', '19<', '11<', '$ 12,.2f>'),
    header_widths=('10<', '50^', '19<', '11<', '12> ($)')
)
```

## TableFormatter
A `TableFormatter` object is an ABC that defines how to write headers, rows, and footers to various output streams.  TableFormatter objects require that all data objects passed to it inherit from TableFormatterDataProvider.

## TableFormatterDataProvider
A TableFormatterDataProvider is an ABC which defines the data to be formatted by the TableFormatter.

## Example:
Imagine we have created a class that represents data about a person.  Now we would like to display a list of `Person` objects using table formatters.  This can be broken into two parts: the formatter and the data provider.

### TableFormatterDataProvider
The following example illustrates how to implement a table formatter data provider.

```
from table_formatters import create_formatter, TableFormatterDataProvider

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
```

### TableFormatter
The following example illustrates  how to implement a custom TableFormatter that will output the table using the python logger.  Note: you must register the `TableFormatter` using the `register_formatter` decorator.  The name specified in the `register_formatter` decorator will be the string used to instanciate the object using `create_formatter` or `create_formatters`.

```
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
```

### Putting it all together
```
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
```
_--- or ---_
```
for idx, person in enumerate(person):
    if idx == 0:
        formatter.header(person)
    formatter.row(person)
formatter.footer('footer col 1, 'footer col 2', 'footer col 3')
```

## Column Width Mini-Language
Column widths are defined as strings in the format
    `<prefix><padding><alignment><suffix>`

__prefix:__ The value to prefix to each message

__padding:__ The width of the column in [Format Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec)

For example: `12` _-- or --_ `11,.2f`
        
__alignment:__ Specifies the column alignment.  See [Formating Specification Mini-Language](https://docs.python.org/3/library/string.html#formatspec) for more information

| Option | Meaning |
| ------ |---------|
| < | Forces the field to be left-aligned within the available space (this is the default for most objects) |
| > | Forces the field to be right-aligned within the available space (this is the default for numbers). |
| = | Forces the padding to be placed after the sign (if any) but before the digits. This is used for printing fields in the form ‘+000000120’. This alignment option is only valid for numeric types. It becomes the default when ‘0’ immediately precedes the field width. |
| ^ | Forces the field to be centered within the available space. |

__suffix:__ The value to append to the message

### Column Width Examples
The string `$ 12,.2f>` will format the column with a width of 12, as a float, using two decimal place precision, and aligned right

The string `50^` will format the column with a width of 50, with center alignment
