# htmltableformatter.py

from ..register_formatter import register_formatter
from ..tableformatter import StringTableFormatter

from utils import memoized

@register_formatter('html')
class HtmlTableFormatter(StringTableFormatter):
    def __init__(self, class_name=None, id=None, **kwargs):
        super().__init__(**kwargs)

        self.__spacer = '    '
        self.__class_name = class_name
        self.__id = id

        self.reset()

    ##########################################################
    # StringTableFormatter ABC Implementation
    ##########################################################

    @property
    def output(self):
        if self.__output:
            return self.__output
    
        elements = ['table']
        if self.__class_name:
            elements.append('class="{}"'.format(self.__class_name))
        if self.__id:
            elements.append('id="{}"'.format(self.__id))
        output = ['<{}>'.format(' '.join(elements))]

        self.__thead.append('{}{}'.format(self.__spacer, '</thead>'))
        self.__tbody.append('{}{}'.format(self.__spacer, '</tbody>'))
        self.__tfoot.append('{}{}'.format(self.__spacer, '</tfoot>'))

        if len(self.__thead) > 1:
            output.extend(self.__thead)
        output.extend(self.__tbody)
        
        if len(self.__tfoot) > 1:
            output.extend(self.__tfoot)
        output.append('</table>')
        
        self.__output = '\n'.join(output)
        return self.__output

    def reset(self):
        '''Resets the output to its initial starting state'''
        self.__thead = ['{}{}'.format(self.__spacer, '<thead>')]
        self.__tbody = ['{}{}'.format(self.__spacer, '<tbody>')]
        self.__tfoot = ['{}{}'.format(self.__spacer, '<tfoot>')]
        self.__output = None

    ##########################################################
    # TableFormatter ABC Implementation
    ##########################################################

    def header(self, data):
        '''Appends header values to the html table'''

        # if headers have been disabled, stop
        if not super().header(data):
            return

        self.__thead.extend(
            self.__format_html_row(data.header_values, 
                self.header_widths, is_header=True)
        )

    def row(self, data):
        if not super().row(data):
            return

        self.__tbody.extend(
            self.__format_html_row(data.row_values, self.column_widths)
        )

    def footer(self, *footers):
        if not super().footer(*footers):
            return

        self.__tfoot.extend(
            self.__format_html_row(footers, self.footer_widths)
        )

    ##########################################################
    # Helper Methods
    ##########################################################

    def __format_html_row(self, data, column_widths, is_header=False):
        tag = 'th' if is_header else 'td'

        output = [self.__spacer * 2 + '<tr>']

        for d, cw in zip(data, column_widths):
            output.append('{3}<{0} {2}>{1}</{0}>'.format(
                tag,
                cw.format(d, resize=False),
                self.__get_style(cw),
                self.__spacer * 3
            )
        )
        output.append(self.__spacer * 2 + '</tr>')
        return output

    @classmethod
    def __get_style(cls, column_width):
        attrs = []

        attrs.append('width: {}px'.format(column_width.width))

        if column_width.alignment:
            attrs.append('text-align: {}'.format(
                'left' if column_width.alignment == '<' else
                'center' if column_width.alignment == '^' else
                'right'
                )
            )
        return 'style="{0}"'.format(';'.join(attrs))