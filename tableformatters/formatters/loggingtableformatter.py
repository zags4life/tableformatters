# table_formatters/loggingtableformatter.py

import logging

from ..register_formatter import register_formatter
from ..tableformatter import TableFormatter

@register_formatter('logger')
@register_formatter('logging')
class LoggerTableFormatter(TableFormatter):
    def __init__(self, logger, log_level, **kwargs):
        super().__init__(**kwargs)
        self.__func = self.__get_logging_func(logger, log_level)

    ##########################################################
    # TableFormatter ABC Implementation
    ##########################################################

    def header(self, data):
        if not super().header(data):
            return

        self.__func(' '.join(self._format_msg(data.header_values, self.header_widths)))

    def row(self, data):
        if not super().row(data):
            return
        self.__func(' '.join(self._format_msg(data.row_values, self.column_widths)))

    def footer(self, *values):
        if not super().footer(*values):
            return
        self.__func(' '.join(self._format_msg(values, self.column_widths)))

    ##########################################################
    # Helper Methods
    ##########################################################

    @staticmethod
    def __get_logging_func(logger, log_level):
        '''Gets the cooresponding logger function bases on the log level
        
        Parameters:
            logger - an instance of LoggerTableFormatter
            log_level - the log level 
        '''
        if isinstance(log_level, str):
            log_level = getattr(logging, log_level.upper())
        
        return getattr(logger, log_level)