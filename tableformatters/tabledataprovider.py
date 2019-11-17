# table_formatters/data_provider.py
from abc import ABC, abstractproperty

class TableFormatterDataProvider(ABC):
    '''An ABC that defines the interface for objects to display by a table
    formatter.  Any object displayed by a TableFormatters must implement this
    ABC.  
    
    Classes that implement this ABC can using this interface to
    define what data contained in its class to display
    '''
    
    @abstractproperty
    def header_values(self):
        '''Must return a list of strings, containing the table header values.
        Note: order of this list is the order that headers will appear'''
        pass
        
    @abstractproperty
    def row_values(self):
        '''Must return a list of data to be output by a table formatter.'''
        pass