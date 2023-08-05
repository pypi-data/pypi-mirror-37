# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: ellen.teradata@teradata.com
Secondary Owner:

This file implements the dataframe locator indexer.
"""
import numbers
import teradataml.dataframe as tdmldf

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import PythonTypes
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.common.aed_utils import AedUtils

class _LocationIndexer():
    """
    Indexer class to access a group of rows and columns by label(s) or a boolean array.

    VALID INPUTS:

        - A single label, e.g. ``5`` or ``'a'``, (note that ``5`` is
        interpreted as a label of the index, it is not interpreted as an
        integer position along the index).

        - A list or array of column or index labels, e.g. ``['a', 'b', 'c']``.

        - A slice object with labels, e.g. ``'a':'f'``.
        Note that unlike the usual python slices where the stop index is not included, both the
            start and the stop are included

        - A conditional expression for row access.

        - A boolean array of the same length as the column axis for column access,

    RETURNS:
        Teradata Machine Learning DataFrame

    RAISE:
        TeradataMlException

    EXAMPLES
    --------
        >>> df = DataFrame('sales')
        >>> df
                      Feb   Jan   Mar   Apr    datetime
        accounts
        Blue Inc     90.0    50    95   101  2017-04-01
        Alpha Co    210.0   200   215   250  2017-04-01
        Jones LLC   200.0   150   140   180  2017-04-01
        Yellow Inc   90.0  None  None  None  2017-04-01
        Orange Inc  210.0  None  None   250  2017-04-01
        Red Inc     200.0   150   140  None  2017-04-01

        Retrieve row using a single label.
        >>> df.loc['Blue Inc']
                   Feb Jan Mar  Apr    datetime
        accounts
        Blue Inc  90.0  50  95  101  2017-04-01

        List of labels. Note using ``[[]]``
        >>> df.loc[['Blue Inc', 'Jones LLC']]
                     Feb  Jan  Mar  Apr    datetime
        accounts
        Blue Inc    90.0   50   95  101  2017-04-01
        Jones LLC  200.0  150  140  180  2017-04-01

        Single label for row and column (index)
        >>> df.loc['Yellow Inc', 'accounts']
        Empty DataFrame
        Columns: []
        Index: [Yellow Inc]

        Single label for row and column
        >>> df.loc['Yellow Inc', 'Feb']
            Feb
        0  90.0

        Single label for row and column access using a tuple
        >>> df.loc[('Yellow Inc', 'Feb')]
            Feb
        0  90.0

        Slice with labels for row and single label for column. As mentioned
        above, note that both the start and stop of the slice are included.
        >>> df.loc['Jones LLC':'Red Inc', 'accounts']
        Empty DataFrame
        Columns: []
        Index: [Orange Inc, Jones LLC, Red Inc]

        Slice with labels for row and single label for column. As mentioned
        above, note that both the start and stop of the slice are included.
        >>> df.loc['Jones LLC':'Red Inc', 'Jan']
            Jan
        0  None
        1   150
        2   150

        Slice with labels for row and labels for column. As mentioned
        above, note that both the start and stop of the slice are included.
        >>> df.loc['Jones LLC':'Red Inc', 'accounts':'Apr']
                     Mar   Jan    Feb   Apr
        accounts
        Orange Inc  None  None  210.0   250
        Red Inc      140   150  200.0  None
        Jones LLC    140   150  200.0   180

        Empty slice for row and labels for column.
        >>> df.loc[:, :]
                      Feb   Jan   Mar    datetime   Apr
        accounts
        Jones LLC   200.0   150   140  2017-04-01   180
        Blue Inc     90.0    50    95  2017-04-01   101
        Yellow Inc   90.0  None  None  2017-04-01  None
        Orange Inc  210.0  None  None  2017-04-01   250
        Alpha Co    210.0   200   215  2017-04-01   250
        Red Inc     200.0   150   140  2017-04-01  None

        Conditional expression
        >>> df.loc[df['Feb'] > 90]
                      Feb   Jan   Mar   Apr    datetime
        accounts
        Jones LLC   200.0   150   140   180  2017-04-01
        Red Inc     200.0   150   140  None  2017-04-01
        Alpha Co    210.0   200   215   250  2017-04-01
        Orange Inc  210.0  None  None   250  2017-04-01

        Conditional expression with column labels specified
        >>> df.loc[df['Feb'] > 90, ['accounts', 'Jan']]
                     Jan
        accounts
        Jones LLC    150
        Red Inc      150
        Alpha Co     200
        Orange Inc  None

        Conditional expression with multiple column labels specified
        >>> df.loc[df['accounts'] == 'Jones LLC', ['accounts', 'Jan', 'Feb']]
                   Jan    Feb
        accounts
        Jones LLC  150  200.0

        Conditional expression and slice with column labels specified
        >>> df.loc[df['accounts'] == 'Jones LLC', 'accounts':'Mar']
                   Mar  Jan    Feb
        accounts
        Jones LLC  140  150  200.0

        Conditional expression and boolean array for column access
        >>> df.loc[df['Feb'] > 90, [True, True, False, False, True, True]]
                      datetime   Apr    Feb
        accounts
        Jones LLC   2017-04-01   180  200.0
        Orange Inc  2017-04-01   250  210.0
        Alpha Co    2017-04-01   250  210.0
        Red Inc     2017-04-01  None  200.0
    """

    def __init__(self, df):
        """
        Constructor for _LocationIndexer.

        PARAMETERS:
            df - The dataframe associated with this indexer.

        EXAMPLES:
            df.loc = _LocationIndexer(df)

        RAISES:

        """
        self._df = df
        self._aed_utils = AedUtils()

    def __getitem__(self, key):
        """
        Access a group of rows and columns by label(s) or ColumnExpression

        PARAMETERS:
            key: A single label, list of labels, or slice. 
                 A tuple containing keys for row and columns access.
                 No more than 2 keys in the tuple.
        RETURNS:
            Teradata Machine Learning DataFrame

        EXAMPLES:

        RAISES:
            TeradataMlException
        """
        try:
            if isinstance(key, tuple):
                return self._get_tuple_index(key, self._df)
            else:
                return  self._get_sort_index(key, self._df)
        except TeradataMlException:
            raise
        except Exception as err:
            errcode = MessageCodes.TDMLDF_INFO_ERROR
            msg = Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR)
            raise TeradataMlException(msg, errcode) from err

    def _get_sort_index(self, key, df):
        """
        Access a group of rows by label(s)

        PARAMETERS:
            key: A single label, list of labels, slice, or ColumnExpression. 
            df: Parent DataFrame

        RETURNS:
            Teradata Machine Learning DataFrame

        EXAMPLES:

        RAISES:
            TeradataMlException
        """
        sort_col = df._get_sort_col()

        if isinstance(key, tuple):
            msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format(type(key), "a single label, a list, or a slice")
            raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

        if isinstance(key, tdmldf.sql._SQLColumnExpression):
            filter_expr = key.compile()
            new_nodeid = self._aed_utils._aed_filter(df._nodeid, filter_expr)
            return tdmldf.dataframe.DataFrame._from_node(new_nodeid, df._metaexpr, df._index_label)
        elif isinstance(key, slice):
            if key.start is not None:
                df_utils._validate_sort_col_type(sort_col[1], key.start)
            if key.stop is not None:
                df_utils._validate_sort_col_type(sort_col[1], key.stop)
            
            if key.start is None and key.stop is None:
                sel_cols = [c for c in df.columns]
                return df.select(sel_cols)
            elif key.start is not None and key.stop is not None:
                if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                    filter_expr = "{0} between '{1}' and '{2}'".format(sort_col[0], key.start, key.stop)
                else:
                    filter_expr = "{0} between {1} and {2}".format(sort_col[0], key.start, key.stop)
                new_nodeid = self._aed_utils._aed_filter(df._nodeid, filter_expr)
                return tdmldf.dataframe.DataFrame._from_node(new_nodeid, df._metaexpr, df._index_label)
            elif key.start is not None:
                if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                    filter_expr = "{0} >= '{1}'".format(sort_col[0], key.start)
                else:
                    filter_expr = "{0} >= {1}".format(sort_col[0], key.start)
                new_nodeid = self._aed_utils._aed_filter(df._nodeid, filter_expr)
                return tdmldf.dataframe.DataFrame._from_node(new_nodeid, df._metaexpr, df._index_label)
            else: #key.stop is not None:
                if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                    filter_expr = "{0} <= '{1}'".format(sort_col[0], key.stop)
                else:
                    filter_expr = "{0} <= {1}".format(sort_col[0], key.stop)
                new_nodeid = self._aed_utils._aed_filter(df._nodeid, filter_expr)
                return tdmldf.dataframe.DataFrame._from_node(new_nodeid, df._metaexpr, df._index_label)
        else:
            df_utils._validate_sort_col_type(sort_col[1], key)
            key_list = key
            if not isinstance(key, list):
                key_list = [key_list]

            if len(key_list) == 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)

            if sort_col[1] == PythonTypes.PY_STRING_TYPE:
                key_list = ["'{}'".format(x) for x in key_list]
            index_expr = ",".join(map(str, (key_list)))

            filter_expr = "{0} in ({1})".format(sort_col[0], index_expr)
            new_nodeid = self._aed_utils._aed_filter(df._nodeid, filter_expr)
            return tdmldf.dataframe.DataFrame._from_node(new_nodeid, df._metaexpr, df._index_label)

    def _get_column_index(self, key, df):
        """
        Access a group of columns by label(s)

        PARAMETERS:
            key: A single label, list of labels, slice, or ColumnExpression.
            df: Parent DataFrame

        RETURNS:
            Teradata Machine Learning DataFrame

        EXAMPLES:

        RAISES:
            TeradataMlException
        """
        if isinstance(key, tuple):
            msg = Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_TYPE).format(type(key), "a single label, a list, or a slice")
            raise TeradataMlException(msg, MessageCodes.TDMLDF_UNKNOWN_TYPE)

        columns = [c for c in df.columns]
        if isinstance(key, slice):
            if key.start is not None and not isinstance(key.start, str):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), 
                                        MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
            if key.stop is not None and not isinstance(key.stop, str):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), 
                                        MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
            if key.start is not None and key.start not in columns:
                msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(key.start, columns)
                raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)

            if key.stop is not None and key.stop not in columns:
                msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(key.stop, columns)
                raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)

            if key.start is None and key.stop is None:
                sel_cols = [c for c in df.columns]
                return df.select(sel_cols)
            elif key.start is not None and key.stop is not None:
                start_index = columns.index(key.start)
                stop_index = columns.index(key.stop)
                if stop_index < start_index:
                    msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL).format(key.stop, columns)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_COL)
                key_list = columns[start_index : stop_index + 1]
            elif key.start is not None:
                start_index = columns.index(key.start)
                key_list = columns[start_index :]
            else: #key.stop is not None:
                stop_index = columns.index(key.stop)
                key_list = columns[ : stop_index + 1]

            return df.select(key_list)
        else:
            key_list = key
            if not isinstance(key, list):
                key_list = [key_list]

            if len(key_list) == 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.EMPTY_DF_RETRIEVED), MessageCodes.EMPTY_DF_RETRIEVED)

            if all(isinstance(n, bool) for n in key_list):
                if len(key_list) != len(columns):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), 
                                        MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)
                sel_cols = []
                for i in range (len(key_list)):
                    if key_list[i]:
                        sel_cols.append(columns[i])
                return df.select(sel_cols)
            elif all(isinstance(n, str) for n in key_list):
                return df.select(key_list)
            else:
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES), MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES)

    def _get_tuple_index(self, key, df):
        """
        Access a group of rows and columns by label(s)

        PARAMETERS:
            key: A column name as a string or filter expression (ColumnExpression)
            df: Parent DataFrame

        RETURNS:
            Teradata Machine Learning DataFrame

        EXAMPLES:

        RAISES:
            TeradataMlException
        """
        if len(key) > 2:
            msg = Messages.get_message(MessageCodes.INVALID_ARG_VALUE).format(key, "for key index", "At most 2 key values for sort and/or column keys")
            raise TeradataMlException(msg, MessageCodes.INVALID_ARG_VALUE)
        if len(key) == 0: 
            sort_index = None
            column_index = [c for c in df.columns]
        elif len(key) == 1:
            sort_index = key[0]
            column_index = None
        else: #len(key) == 2
            sort_index = key[0]
            column_index = key[1]

        if sort_index is not None:
            new_df = self._get_sort_index(sort_index, df)
        else:
            new_df = df

        if column_index is not None:
            return self._get_column_index(column_index, new_df)
        else:
            return new_df
