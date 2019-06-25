# table_formatters/loggingtableformatter.py

import logging

from ..register_formatter import register_formatter
from ..tableformatter import TableFormatter

@register_formatter('logger')
class LoggerTableFormatter(TableFormatter):
    def __init__(self, logger, log_level, **kwargs):
        super().__init__(**kwargs)
        self.__func = self.__get_logging_func(logger, log_level)

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

    @classmethod
    def __get_logging_func(self, logger, log_level):
        if log_level == logging.ERROR or log_level == 'error':
            return logger.error
        if log_level == logging.WARNING or log_level == 'warning':
            return logger.warning
        if log_level == logging.INFO or log_level == 'info':
            return logger.info
        if log_level == logging.DEBUG or log_level == 'debug':
            return logger.debug
        raise AssertionError("Unknown log_level '{}'".format(log_level))