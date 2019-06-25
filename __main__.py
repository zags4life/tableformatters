# table_formatters/__main__.py

import logging

from .compositetableformatter import CompositeTableFormatter
from .create_formatter import create_formatter
from .tabledataprovider import TableFormatterDataProvider

def main():

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

    logger = logging.getLogger('LoggerTableFormatter')

    info_formatter = create_formatter(
        formatter_type='csv',
        logger=logger,
        log_level='info',
        filename='foo.csv',
        column_widths=('12<', '50<', '12<', '12<', '12<')
    )

    formatter = CompositeTableFormatter()
    formatter.add_formatter(info_formatter)

    persons = [
        Person('Mike Smith', '123 Fake St', '3125551212'),
        Person('Tom Smith', '456 Fake St', '3124567890')
    ]

    total = 0
    with formatter:
        for data in formatter.writelines(persons):
            total += 1
        formatter.footer('Total', ' ', total)


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    main()