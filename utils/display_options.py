# table_formatters/display_options.py

from enum import Enum

class DisplayOptions(Enum):
    '''An enumeration used to specify which data is to be displayed.

    This is particularly needed for composite formatters where each child
    formatter has difference display options
    '''
    Headers = "headers"
    Rows = "rows"
    Footers = "footers"
