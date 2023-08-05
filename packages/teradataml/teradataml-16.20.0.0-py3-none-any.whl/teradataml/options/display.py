"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: karthik.thelukuntla@teradata.com
Secondary Owner: mark.sandan@teradata.com

This file is for providing user configurable options.
"""

class _Display(object):
    """
    Display options for printing teradataml DataFrames and SQLMR functions.
    """

    def __init__(self,
                 max_rows = 10,
                 precision = 3,
                 byte_encoding = 'base16',
                 print_sqlmr_query = False):

        self.max_rows = max_rows
        self.precision = precision
        self.byte_encoding = byte_encoding
        self.print_sqlmr_query = print_sqlmr_query

    @property
    def max_rows(self):
        """default number of rows for head() and print()"""
        return self.__max_rows

    @max_rows.setter
    def max_rows(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError('max_rows must be a positive int.')

        self.__max_rows = value

    @property
    def precision(self):
        """Round DECIMAL and/or NUMBER types when printing a DataFrame"""
        return self.__precision

    @precision.setter
    def precision(self, value):
        if (not isinstance(value, int) or value <= 0):
            raise ValueError('precision must be a positive int.')

        self.__precision = value

    @property
    def byte_encoding(self):
        """
        The encoding used for printing byte-like types in a DataFrame
        """

        return self.__byte_encoding

    @byte_encoding.setter
    def byte_encoding(self, value):
        valid_encodings = ('ascii', 'base16', 'base2', 'base8', 'base64M')
        if not isinstance(value, str) or (not value.lower().startswith('base') and  value.lower() != 'ascii'):
            err = 'byte_encoding must be a string that is a valid encoding (e.g. {}).'.format(valid_encodings)
            raise ValueError(err)

        self.__byte_encoding = value

    @property
    def print_sqlmr_query(self):
        """
        prints the SQLMR query when a SQLMR function is called if True
        """
        return self.__print_sqlmr_query

    @print_sqlmr_query.setter
    def print_sqlmr_query(self, value):
        if not isinstance(value, bool):
            raise ValueError('print_sqlmr_query must be True/False.')

        self.__print_sqlmr_query = value


display = _Display()
