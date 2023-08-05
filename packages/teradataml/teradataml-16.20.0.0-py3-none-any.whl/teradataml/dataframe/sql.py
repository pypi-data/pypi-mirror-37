# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner:
Secondary Owner:

"""
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.options.display import display
from .sql_interfaces import TableExpression, ColumnExpression
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy import Table, Column, literal, MetaData, func, or_, and_, literal_column
import functools
import re

from teradatasqlalchemy.dialect import dialect as td_dialect, compiler as td_compiler
from teradatasqlalchemy import (INTEGER, SMALLINT, BIGINT, BYTEINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy import (DATE, TIME, TIMESTAMP)
from teradatasqlalchemy import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)
import decimal
import datetime as dt

def _resolve_value_to_type(value):
    """
    Internal function for coercing python literals to sqlalchemy_terdata types
    or retrieving the derived type of ColumnExpression

      Parameters
      ----------
          value: a python literal type or ColumnExpression instance

      Returns
      ----------
          result: sqlalchemy TypeEngine derived type or ColumnExpression derived type

      Note: Currently the supported literal types are str/float/int/decimal
            since these are being rendered already by teradatasqlalchemy
    """
    type_map = {
      str: VARCHAR(TeradataConstants['DEFAULT_VAR_SIZE'].value, charset = 'UNICODE'),
      bytes: VARBYTE(TeradataConstants['DEFAULT_VAR_SIZE'].value),
      int: INTEGER(),
      float: FLOAT(),
      bool: BYTEINT(),
      decimal.Decimal: DECIMAL(38,37),
      dt.date: DATE(),
      dt.datetime: TIMESTAMP(),
      dt.time: TIME()
    }

    result = type_map.get(type(value))

    if isinstance(value, ColumnExpression):
      result = value.type
    return result

def _handle_sql_error(f):
    """
      This decorator wraps python special methods that generate SQL for error handling.
      Any error messages or error codes involving sql generating methods
      can be considered here.

      Parameters
      ----------
        A function or method that generates sql

      Ezamples
      --------
          @_handle_sql_error
          def __and__(self, other)

    """
    @functools.wraps(f)
    def inner(*args, **kw):

      try:

        self_ = None
        other_ = None

        if len(args) == 2:
          self_, other_ = args

        if self_ is not None and other_ is not None and\
           isinstance(self_, ColumnExpression) and\
           isinstance(other_, ColumnExpression) and\
           self_.table is not None and other_.table is not None:

          if self_.table.name != other_.table.name or\
             self_.table.schema != other_.table.schema:
               raise ValueError('Combining Columns from different tables is unsupported')

        res = f(*args, **kw)

      except Exception as err:

        errcode = MessageCodes.TDMLDF_INFO_ERROR
        msg = Messages.get_message(errcode)
        raise TeradataMlException(msg, errcode) from err

      return res
    return inner


class _MetaExpression(object):
    """
    The _MetaExpression contains the TableExpression and provides the DataFrame with metadata
    from the underlying Table as well as methods for translating and generating SQL.

    The main responsibility of this class is to translate sql expressions internally in DataFrame.
    Other responsibilities are delegated to the underlying TableExpression.

    This class is internal.
    """

    def __init__(self, table, **kw):
      """
        Parameters
        ----------
            table: the table to use for TableExpression

            kw: kwargs for implementation specific TableExpressions/ColumnExpressions
              - dialect: an implementation of a SQLAlchemy Dialect
      """

      self._dialect = kw.get('dialect', td_dialect())
      self.__t = _SQLTableExpression(table, **kw)

    def __getattr__(self, key):

      """
      Retrieve an attribute from _MetaExpression or the underlying TableExpression

        Parameters
        ----------
            key: attribute name

        Raises
        -------
        AttributeError if attribute can't be found
      """

      res = getattr(self.__t, key, None)
      if res is None:
        raise AttributeError('Unable to find attribute: %s' % key)

      return res

    def __repr__(self):
      return repr(self.__t)

class _PandasTableExpression(TableExpression):

    def _assign(self, drop_columns, **kw):
      """
      Internal method for DataFrame.assign
      Generates the new select list column expressions and
      provides an updated _SQLTableExpression for the new _MetaExpression

        Raises
        ------
        ValueError when a value that is callable is given in kwargs


        See Also
        --------
          DataFrame.assign


        Returns
        -------
        result : -Updated _SQLTableExpression
                 -list of compiled column expressions

      Note: This method assumes that the values in each key of kw
            are valid types (supported python literals or ColumnExpressions)
      """
      compiler = td_compiler(td_dialect(), None)
      current = {c.name for c in self.c}

      assigned_expressions = []

      existing = [(c.name, c) for c in self.c]
      new = [(label, expression) for label, expression in kw.items() if label not in current]
      new = sorted(new, key = lambda x: x[0])

      for alias, expression in existing + new:
        if drop_columns and alias not in kw:
            continue

        else:
            expression = kw.get(alias, expression)
            type_ = _resolve_value_to_type(expression)

            if not isinstance(expression, ColumnExpression):
              # wrap literals. See DataFrame.assign for valid literal values
              expression = _SQLColumnExpression(literal(expression, type_ = type_))

            aliased_expression = compiler.visit_label(expression.expression.label(alias),
                                                      within_columns_clause=True,
                                                      include_table = False,
                                                      literal_binds = True)
            assigned_expressions += [(alias, aliased_expression, type_)]

      if len(assigned_expressions) >= TeradataConstants['TABLE_COLUMN_LIMIT'].value:
          raise ValueError('Maximum column limit reached')

      cols = (Column(name, type_) for name, expression, type_ in assigned_expressions)
      t = Table(self.name, MetaData(), *cols)

      return (_SQLTableExpression(t), assigned_expressions)


    def _filter(self, axis, op, index_labels, **kw):
        """
        Subset rows or columns of dataframe according to labels in the specified index.

        Parameters:
          axis: int
            1 for columns to filter
            0 for rows to filter

          op: string
            A string representing the way to index.
            This parameter is used along with axis to get the correct expression.

          index_labels: list or iterable of string
            contains column names/labels of the DataFrame

          **kw: keyword arguments
            items: None or a list of strings
            like: None or a string representing a substring
            regex: None or a string representing a regex pattern

            optional keywords:
              match_args: string of characters to use for REGEXP_SUBSTR

        Returns:
            tuple of two elements:
              Either a tuple of (list of str, 'select') if axis == 1
              Or a tuple of (list of ColumnExpressions, 'where') if axis == 0

        Note:
          Implementation outline:

          axis == 1 (column based filter)

            items - [colname for colname in colnames if colname in items]
            like - [colname for colname in colnames if like in colname]
            regex - [colname for colname in colnames if re.search(regex, colname) is not None]

          axis == 0 (row value based filter on index)

            items - WHERE index IN ( . . . )
            like -  same as regex except the string (kw['like']) is a substring pattern
            regex - WHERE REGEXP_SUBSTR(index, regex, 1, 1, 'c')


        Examples:

          # self is a reference to DataFrame's _metaexpr.
          # This method is usually called from the DataFrame.
          # Suppose the DataFrame has columns ['a', 'b', 'c'] in its index:

          # select columns given in items list
          self._filter(1, 'items', ['a', 'b', 'c'], items = ['a', 'b'])

          # select columns matching like pattern (index_labels is ignored)
          self._filter(1, 'like', ['a', 'b', 'c'], like = 'substr')

          # select columns matching regex pattern (index_labels is ignored)
          self._filter(1, 'regex', ['a', 'b', 'c'], regex = '[0|1]')

          # select rows where index column(s) are in items list
          self._filter(0, 'items', ['a', 'b', 'c'], items = [('a', 'b', 'c')])

          # select rows where index column(s) match the like substring
          self._filter(0, 'like', ['a', 'b', 'c'], like = 'substr')

          # select rows where index column(s) match the regex pattern
          self._filter(0, 'regex', ['a', 'b', 'c'], regex = '[0|1]')
        """

        impls = dict({

            ('like', 1):  lambda col: kw['like'] in col.name,

            ('regex', 1): lambda col: re.search(kw['regex'], col.name) is not None,

            ('items', 0): lambda colexp, lst: colexp.in_(lst),

            ('like', 0):  lambda colexp: func.regexp_substr(colexp, kw['like'], 1, 1,
                                                            kw.get('match_arg', 'c')) != None,

            ('regex', 0): lambda colexp: func.regexp_substr(colexp, kw['regex'], 1, 1,
                                                            kw.get('match_arg', 'c')) != None
          }
        )

        filtered_expressions = []
        filter_ = impls.get((op, axis))
        is_char_like = lambda x: isinstance(x, CHAR) or\
                                 isinstance(x, VARCHAR) or\
                                 isinstance(x, CLOB)
        if axis == 1:

            # apply filtering to columns and then select()
            if op == 'items':

              for col in kw['items']:
                  filtered_expressions += [col]

            else:

              for col in self.c:
                if filter_(col):
                  filtered_expressions += [col.name]

        else:
            # filter based on index values
            # apply filtering to get appropriate ColumnExpression then __getitem__()

            if op == 'items':

                if len(index_labels) == 1:

                  # single index case
                  for c in self.c:
                    if c.name in index_labels:

                      expression = c.expression
                      filtered_expressions += [filter_(expression, kw['items'])]

                else:

                  # multi index case
                  items_by_position = zip(*kw['items'])

                  # traverse in the order given by index_label
                  for index_col, item in zip(index_labels, items_by_position):
                    for c in self.c:
                      if c.name == index_col:

                        expression = c.expression
                        filtered_expressions += [filter_(expression, item)]

            else:

                var_size = kw.get('varchar_size',  TeradataConstants['DEFAULT_VAR_SIZE'].value)
                for c in self.c:
                  if c.name in index_labels:

                    expression = c.expression
                    if not is_char_like(expression.type):
                      # need to cast to char-like operand for REGEXP_SUBSTR
                      expression = expression.cast(type_ = VARCHAR(var_size))

                    filtered_expressions += [filter_(expression)]

            if axis == 0:

                if op == 'items' and len(index_labels) > 1:

                    # multi index item case is a conjunction
                    filtered_expressions = _SQLColumnExpression(and_(*filtered_expressions))

                else:
                    filtered_expressions = _SQLColumnExpression(or_(*filtered_expressions))

        return filtered_expressions


class _SQLTableExpression(_PandasTableExpression):
    """
      This class implements TableExpression and is contained
      in the _MetaExpressions class

      It handles:
        - SQL generation for the table or all it's columns
        - DataFrame metadata access using a sqlalchemy.Table

      This class is internal.
    """
    def __init__(self, table, **kw):

        """
          Initialize the _SQLTableExpression

          Parameters
            ----------
            table : A sqlalchemy.Table
            kw**: a dict of optional parameters
              - column_order: a collection of string column names
                              in the table to be ordered in the c attribute

        """

        self.t = table
        if 'column_order' in kw:
            # Use DataFrame.columns to order the columns in the metaexpression
            columns = []
            for c in kw['column_order']:
                name = c.strip()
                col = table.c.get(name, table.c.get(name.lower(), table.c.get(name.upper())))

                if col is None:
                  raise ValueError('Reflected column names do not match those in DataFrame.columns')

                columns.append(_SQLColumnExpression(col))

            self.c = columns

        else:
            self.c = [_SQLColumnExpression(c) for c in table.c]

    @property
    def c(self):
      """
      Returns the underlying collection of _SQLColumnExpressions
      """
      return self.__c

    @c.setter
    def c(self, collection):
      """
      Set the underlying map of _SQLColumnExpressions

      Parameters
      ----------
        collection: a dict of _SQLColumnExpressions

      """
      is_sql_colexpression = lambda x: type(x) == _SQLColumnExpression
      valid_collection = isinstance(collection, list) and\
                         len(collection) > 0 and\
                         all(map(is_sql_colexpression, collection))

      if (not valid_collection):
        raise ValueError("collection must be a non empty list of _SQLColumnExpression instances. Got {}".format(collection))


      self.__c = collection

    @property
    def name(self):
      """
      Returns the name of the underlying SQLAlchemy Table
      """
      return self.t.name

    @property
    def t(self):
      """
      Returns the underlying SQLAlchemy Table
      """
      return self.__t

    @t.setter
    def t(self, table):
      """
      Set the underlying SQLAlchemy Table

      Parameters
      ----------
        table : A sqlalchemy.Table
      """
      if (not isinstance(table, Table)):
        raise ValueError("table must be a sqlalchemy.Table")

      self.__t = table

    def __repr__(self):
      """
      Returns a SELECT TOP string representing the underlying table.
      For representation purposes:
        - the columns are cast into VARCHAR
        - certain numeric columns are first rounded
        - character-like columns are unmodfied
        - byte-like columns are called with from_bytes to show them as ASCII


      Notes:
        - The top integer is taken from teradataml.options
        - The rounding value for numeric types is taken from teradataml.options
        - from_bytes is called on byte-like columns to represent them as ASCII encodings
          See from_bytes for more info on different encodings supported:
          Teradata® Database SQL Functions, Operators, Expressions, and Predicates, Release 16.20

      """
      # TODO: refactor this to be in the ColumnExpression instances
      single_quote = literal_column("''''")
      from_bytes = lambda c: ('b' + single_quote + func.from_bytes(c, display.byte_encoding) + single_quote).label(c.name)
      display_decimal = lambda c: func.round(c, display.precision).cast(type_ = DECIMAL(38, display.precision)).label(c.name)
      display_number = lambda c: func.round(c, display.precision).label(c.name)

      compiler = td_compiler(td_dialect(), None)
      var_size = TeradataConstants['DEFAULT_VAR_SIZE'].value
      cast_expr = lambda c: c.cast(type_ = VARCHAR(var_size)).label(c.name)

      res = 'select top {} '.format(display.max_rows)
      expressions = []

      for c in self.c:

        if isinstance(c.type, (CHAR, VARCHAR, CLOB, FLOAT)):
          expression = c.expression.label(c.name)

        elif isinstance(c.type, (BYTE, VARBYTE, BLOB)):
          expression = from_bytes(c.expression)

        elif isinstance(c.type, DECIMAL):
          expression = cast_expr(display_decimal(c.expression))

        elif isinstance(c.type, NUMBER):
          expression = cast_expr(display_number(c.expression))

        else:
          expression = cast_expr(c.expression)

        expressions.append(compiler.visit_label(expression,
                                                within_columns_clause=True,
                                                include_table = False,
                                                literal_binds = True))

      return res + ', '.join(expressions)

class _LogicalColumnExpression(ColumnExpression):

    """
      The _LogicalColumnExpression implements the logical special methods
      for _SQLColumnExpression.
    """

    @_handle_sql_error
    def __and__(self, other):

      """
        Compute the logical and between two column expressions using &

        Parameters
        ----------
            other : A python literal or another ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[(c1 > 0) & (c2 > 0)]
        df[(c1 > 0) & (c2 > 0) & (c1 > c2)]

      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression & expr)
      return res

    @_handle_sql_error
    def __rand__(self, other):
      """
      Reverse and
      See __and__
      """
      return self & other

    @_handle_sql_error
    def __or__(self, other):

      """
        Compute the logical or between two column expressions using |


        Parameters
        ----------
            other : literal or ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        See Also
        --------

        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[(c1 > 0) | (c2 > 0)]
        df[(c1 > 0) | (c2 > 0) | (c1 > c2)]
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression | expr)
      return res

    @_handle_sql_error
    def __ror__(self, other):
      """
      Reverse or
      See __or__
      """
      return self | other

    @_handle_sql_error
    def __invert__(self):

      """
        Compute the logical not between two column expressions using ~


        Parameters
        ----------
            self

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        See Also
        --------

        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[~(c1 > 0)]
        df[~((c1 > 0) | (c2 > 0))]
      """
      return _SQLColumnExpression(~self.expression)

    @_handle_sql_error
    def __gt__(self, other):

      """
        Compare the column expression using >

        Parameters
        ----------
            values : A python literal or another ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[c1 > 0]
        df[(c1 > 0) & (c2 > c1)]

      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression > expr)
      return res


    @_handle_sql_error
    def __lt__(self, other):

      """
        Compare the column expression using <

        Parameters
        ----------
            values : A python literal or another ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[c1 < 0]
        df[(c1 < 0) & (c2 < c1)]

      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression < expr)
      return res

    @_handle_sql_error
    def __ge__(self, other):

      """
        Compare the column expression using >=


        Parameters
        ----------
            values : A python literal or another ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression


        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[c1 >= 0]
        df[(c1 >= 0) & (c2 >= c1)]
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression >= expr)
      return res

    @_handle_sql_error
    def __le__(self, other):

      """
        Compare the column expression using <=

        Parameters
        ----------
            values : A python literal or another ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        Examples
        --------
        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[c1 <= 0]
        df[(c1 <= 0) & (c2 <= c1)]
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression <= expr)
      return res

    @_handle_sql_error
    def __xor__(self, other):
      """
        Compute the logical or between two column expressions using ^

        Parameters
        ----------
            exp : A python literal or _SQLColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression


        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[(c1 > 0) ^ (c2 > c1)]
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression((self.expression | expr) & ~(self.expression & expr))
      return res

    @_handle_sql_error
    def __rxor__(self, other):
      """
      Reverse xor
      See __xor__
      """
      return self ^ other

    @_handle_sql_error
    def __eq__(self, other):
      """
        Compute equality using ==

        Parameters
        ----------
            other : A python literal or another _SQLColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression


        Examples
        --------
        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[c1 == 0]
        df[(c1 == 0) & (c2 == c1)]
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression == expr)
      return res

    @_handle_sql_error
    def __ne__(self, other):
      """
        Compute inequality using !=

        Parameters
        ----------
            other : A python literal or another _SQLColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression


        Examples
        --------
        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df[c1 != 0]
        df[(c1 != 0) & (c2 != c1)]
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression != expr)
      return res


class _ArithmeticColumnExpression(ColumnExpression):

    """
      The _ArithmeticColumnExpression implements the arithmetic special methods
      for _SQLColumnExpression.
    """

    @_handle_sql_error
    def __add__(self, other):

      """
        Compute the sum between two column expressions using +


        Parameters
        ----------
            other : literal or ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        See Also
        --------

        Examples
        --------
        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df.assign(x = 1 + c2)
        df.assign(x = c2 + c1)
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression + expr)
      return res

    @_handle_sql_error
    def __radd__(self, other):

      """
        Compute the rhs sum between two column expressions using +


          Parameters
          ----------
          other : literal or ColumnExpression

          Examples
          --------

          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df.assign(x = 1 + c2)
          df.assign(x = c2 + c1)
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(expr + self.expression)
      return res

    @_handle_sql_error
    def __sub__(self, other):

      """
        Compute the difference between two column expressions using -


          Parameters
          ----------
          other : literal or ColumnExpression

          Returns
          -------
          res : _SQLColumnExpression

          Raises
          ------
          Exception
            * A TeradataMlException gets thrown if SQLAlchemy
              throws an exception when evaluating the expression

          Examples
          --------

          df = DataFrame('df')
          c1 = df.c1
          c2 = df.c2
          df.assign(c1_minus_c2 = c1 - c2)
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression - expr)
      return res

    @_handle_sql_error
    def __rsub__(self, other):
      """
        Compute the difference between two column expressions using -
        See __sub__.

      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(expr - self.expression)
      return res

    @_handle_sql_error
    def __mul__(self, other):

      """
        Compute the product between two column expressions using *


        Parameters
        ----------
            other : literal or ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        See Also
        --------

        Examples
        --------

        df = DataFrame('df')
        c1 = df.c1
        c2 = df.c2
        df.assign(c1_x_c2 = c1 * c2)
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression * expr)
      return res

    @_handle_sql_error
    def __rmul__(self, other):

      """
        Compute the product between two column expressions using *
        See __truediv__
      """
      return self * other

    @_handle_sql_error
    def __truediv__(self, other):

      """
        Compute the division between two column expressions using /


        Parameters
        ----------
            other : literal or ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df.assign(c1 /c2)
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression / expr)
      return res

    @_handle_sql_error
    def __rtruediv__(self, other):

      """
        Compute the division between two column expressions using /
        See __truediv__
      """

      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(expr / self.expression)
      return res

    @_handle_sql_error
    def __floordiv__(self, other):

      """
        Compute the floor division between two column expressions using //


        Parameters
        ----------
            other : literal or ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        See Also
        --------

        Examples
        --------

        df = DataFrame(...)
        c1 = df.c1
        c2 = df.c2
        df.assign(floord = c1 // c2)
      """
      raise NotImplementedError()

    @_handle_sql_error
    def __rfloordiv__(self, other):

      """
        Compute the floor division between two column expressions using //
        See __floordiv__
      """
      raise NotImplementedError()

    @_handle_sql_error
    def __mod__(self, other):

      """
        Compute the MOD between two column expressions using %


        Parameters
        ----------
            other : literal or ColumnExpression

        Returns
        -------
            res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        Examples
        --------

        df = DataFrame('df')
        c1 = df.c1
        c2 = df.c2
        df.assign(c1modc2 = c1 % c2)
      """
      expr = other.expression if isinstance(other, _SQLColumnExpression) else other
      res = _SQLColumnExpression(self.expression % expr)
      return res

    @_handle_sql_error
    def __rmod__(self, other):
      """
        Compute the MOD between two column expressions using %
        Note: string types already override the __mod__ . We cannot override it
              if the string type is the left operand.

        See __mod__
      """

      expr = other.expression if isinstance(other, _SQLColumnExpression) else other

      if type(expr) is str:
        raise ValueError('MOD with string literals as the left operand is unsupported')

      res = _SQLColumnExpression(expr % self.expression)
      return res


    @_handle_sql_error
    def __neg__(self):

      """
        Compute the unary negation of the column expressions using -


        Returns
        -------
          res : _SQLColumnExpression

        Raises
        ------
        Exception
          * A TeradataMlException gets thrown if SQLAlchemy
            throws an exception when evaluating the expression

        See Also
        --------

        Examples
        --------

        df = DataFrame(...)

        c1 = df.c1
        a = df[c1 >= 0]

        c1 = -df.c1
        b = df[c1 <= 0]

        a == b
      """
      res = _SQLColumnExpression(-self.expression)
      return res


class _SeriesColumnExpression(ColumnExpression):

    """
      The _SeriesColumnExpression implements the pandas.Series methods
      for _SQLColumnExpression.
    """

    def gt(self, other):
      """
        Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.gt(0)]
          df[c1.gt(0) & c2.gt(c1)]
      """
      return self > other

    def ge(self, other):
      """
        Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.ge(0)]
          df[c1.ge(0) & c2.ge(c1)]
      """
      return self >= other

    def lt(self, other):
      """
        Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.lt(0)]
          df[c1.lt(0) & c2.lt(c1)]
      """
      return self < other

    def le(self, other):
      """
        Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.le(0)]
          df[c1.le(0) & c2.le(c1)]
      """
      return self <= other

    def eq(self, other):
      """
        Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.eq(0)]
          df[c1.eq(0) & c2.eq(c1)]
      """
      return self == other

    def ne(self, other):
      """
        Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.ne(0)]
          df[c1.ne(0) & c2.ne(c1)]
      """
      return self != other

    def add(self, other):
      """
          Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df.assign(add = c1 + c2)
      """
      return self + other

    def sub(self, other):
      """
          Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df.assign(sub = c1.sub(c2))
      """
      return self - other

    def mul(self, other):
      """
          Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df.assign(mul = c1.mul(c2))
      """
      return self * other

    def div(self, other):
      """
          Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df.assign(div = c1.div(c2))
      """
      return self.truediv(other)

    def truediv(self, other):
      """
          Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df.assign(div = c1.truediv(c2))
      """
      return self / other

    def floordiv(self, other):
      """
          Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df.assign(c1_floordiv_c2 = c1.floordiv(c2))
      """
      return self // other

    def mod(self, other):
      """
          Parameters
          ----------
          other : ColumnExpression or literal

          Returns
          -------
            _SQLColumnExpression

          Examples
          --------
          df = DataFrame(...)
          c1 = df.c1
          c2 = df.c2
          df[c1.mod(2)]
          df[c1.mod(c2) == 0 & c2.mod(c1) == 0]
      """
      return self % other


class _SQLColumnExpression(_LogicalColumnExpression,
                           _ArithmeticColumnExpression,
                           _SeriesColumnExpression):

    """
      _SQLColumnExpression is used to build Series/Column manipulations into SQL.
      It represents a column from a Table or an expression involving some operation
      between columns and other literals.

      These objects are created from _SQLTableExpression or from operations
      involving other _SQLColumnExpressions.

      They behave like sqlalchemy.Column objects when accessed from the SQLTableExpression.
      Thus you can access certain common attributes (decorated with property) specified by
      the ColumnExpression interface. Otherwise, the attributes refer to expressions.
      In this case, None is returned if an attribute is not found in the expression.

      This class is internal.
    """

    def __init__(self, expression, **kw):

      """
        Initialize the ColumnExpression

        Parameters
          ----------
          expression : A sqlalchemy.ClauseElement instance.

      """
      self.expression = expression


    @property
    def expression(self):
      """
      A reference to the underlying column expression
      """
      return self.__expression

    @expression.setter
    def expression(self, expression):
      """
      Set a reference to the underlying column expression
      """
      if (not isinstance(expression, ClauseElement)):
        raise ValueError('_SQLColumnExpression requires a sqlalchemy.ClauseElement expression')
      self.__expression = expression

    @property
    def type(self):
      """
        Returns the underlying sqlalchemy type of the current expression.
      """
      return self.expression.type

    @property
    def name(self):
      """
      Returns the underlying name attribute of self.expression or None
      if the expression has no name. Note that the name may also refer to
      an alias or label() in sqlalchemy
      """
      return getattr(self.expression, 'name', None)

    @property
    def table(self):
      """
      Returns the underlying table attribute of the sqlalchemy.Column
      """
      return getattr(self.expression, 'table', None)

    def compile(self, *args, **kw):
      """
      Calls the compile method of the underlying sqlalchemy.Column
      """
      if len(kw) == 0:
        kw = dict({'dialect': td_dialect(),
                   'compile_kwargs':
                           {
                            'include_table': False,
                            'literal_binds': True
                           }
                  })

      return str(self.expression.compile(*args, **kw))

    def __hash__(self):
      return hash(self.expression)
