# table_formatters/__main__.py

from argparse import ArgumentParser
import logging

from .formatters.compositetableformatter import CompositeTableFormatter
from .create_formatter import create_formatters
from .tabledataprovider import TableFormatterDataProvider
from .register_formatter import get_formatter_names

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

    logger = logging.getLogger(__name__)

    formatter = create_formatters(
        formatters='logging;csv',
        logger=logger,
        log_level=logging.DEBUG,
        filename='foo.csv',
        column_widths=('12<', '50<', '12<', '12<', '12<')
    )

    persons = [
        Person('Mike Smith', '123 Fake St', '3125551212'),
        Person('Tom Smith', '456 Fake St', '3124567890')
    ]

    total = 0
    with formatter:
        for data in formatter.writelines(persons):
            total += 1
        formatter.footer('Total', ' ', total)

def print_formatter_names():
    print('Available table formatters:')

    for name in get_formatter_names():
        print(' '*3, name)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser()
    parser.add_argument('--names', action='store_true',
        help='Lists all available table formatters')
    args = parser.parse_args()

    if args.names:
        print_formatter_names()
        exit(0)

    main()