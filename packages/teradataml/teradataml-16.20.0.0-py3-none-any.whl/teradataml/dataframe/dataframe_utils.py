# -*- coding: utf-8 -*-
"""

Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: karthik.thelukuntla@teradata.com
Secondary Owner:

This file implements util functions of data frame.
"""

import re
import numbers

from teradataml.common.utils import UtilFuncs
from teradataml.common.aed_utils import AedUtils
from teradataml.context.context import get_context
from teradataml.common.constants import AEDConstants
from teradataml.common.constants import SQLPattern
import pandas as pd
from teradataml.options.display import display
from teradataml.common.sqlbundle import SQLBundle
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import PythonTypes
from teradataml.context.context import _get_current_databasename
from teradatasqlalchemy.types import FLOAT
from teradatasqlalchemy.types import INTEGER
from teradatasqlalchemy.dialect import preparer, dialect as td_dialect


# TODO - Need to write unit testcases for these functions
class DataFrameUtils():

    @staticmethod
    def _execute_node_return_db_object_name(nodeid):
        """
        Fetches queries and view names from AED node and creates views from queries

        PARAMETERS:
            None

        EXAMPLES:
             _execute_node_return_db_object_name(nodeid)

        RETURNS:
            Top level view name.

        """
        aed_obj = AedUtils()
        if not aed_obj._aed_is_node_executed(nodeid):
            view_query_node_type_list = aed_obj._aed_get_exec_query(nodeid)
            view_names = view_query_node_type_list[0]
            queries = view_query_node_type_list[1]
            node_query_types = view_query_node_type_list[2]
            node_ids = view_query_node_type_list[3]

            # Executing Nodes / Creating Views
            for index in range(len(queries) - 1, -1, -1):
                try:
                    if node_query_types[index] == AEDConstants.AED_QUERY_NODE_TYPE_ML_QUERY_MULTI_OUTPUT.value or \
                            (SQLPattern.SQLMR.match(queries[index]) and "OUT TABLE " in queries[index]):
                        # TODO:: OR condition in above needs to be removed once AED support is added.
                        # Driver function. Table needs to be created.
                        UtilFuncs._create_table(view_names[index], queries[index])
                    elif node_query_types[index] == AEDConstants.AED_QUERY_NODE_TYPE_REFERENCE.value:
                        # Reference nodes - To be ignored.
                        pass
                    else:
                        UtilFuncs._create_view(view_names[index], queries[index])
                    # Updating Node Status for executed Node
                    aed_obj._aed_update_node_state_single(node_ids[index], AEDConstants.AED_NODE_EXECUTED.value)
                except Exception as emsg:
                    # TODO:: Append node execution details to emsg.
                    #        Node descritpion, such as nodeType or node operation, should be added
                    #        here in 'emsg' to give away more information, where exactly
                    #        node execution failed.
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED)

        # Setting New Table name retrieved to TDML DF
        return aed_obj._aed_get_tablename(nodeid)

    @staticmethod
    def _get_dataframe_print_string(table_name, index_label, orderby = None, undropped_index=None):
        """
        Builds string output for TeradataML DataFrame

        PARAMETERS:
            table_name - Name of the database table to read from.
            index_label - String/List specifying column to use as index.
            orderby - order expression to sort returned rows

        EXAMPLES:
             _get_dataframe_print_string('table_name', None, None)

        RETURNS:
            String representation of a pandas DataFrame.

        """
        read_query = SQLBundle._build_top_n_print_query(table_name, display.max_rows, orderby)

        if index_label:
            pandas_df = pd.read_sql_query(read_query, get_context(), index_col = index_label)
        else:
            pandas_df = pd.read_sql_query(read_query, get_context())

        return pandas_df.to_string()

    @staticmethod
    def _get_pprint_dtypes(column_names_and_types, null_count=False):
        """
        returns a string containing the column names and types.
        If null_count is not None, the string will also contain
        the number of non-null values for each column.

        PARAMETERS:
            column_names_and_types - List of column names and types.
            null_count(optional) - List of the non-null count for each column.

        EXAMPLES:
            >>>print(_get_pprint_dtypes(column_names_and_types)
            accounts      str
            Feb         float
            Jan           int
            Mar           int
            Apr           int
            datetime      str

            >>>print(_get_pprint_dtypes(column_names_and_types, null_count)
            accounts    3 non-null str
            Feb         3 non-null float
            Jan         3 non-null int
            Mar         3 non-null int
            Apr         3 non-null int
            datetime    3 non-null str

        RAISES:

        """

        col_names = [i[0] for i in column_names_and_types]
        col_types = [i[1] for i in column_names_and_types]
        max_col_names = len(max(col_names, key=len)) + 4
        max_col_types = len(max(col_types, key=len))
        dtypes_string = ""
        if not null_count:
            for colname, coltype in column_names_and_types:
                dtypes_string += "{0: <{name_width}}{1: >{type_width}}\n".format(colname, coltype,
                                                                                 name_width=max_col_names,
                                                                                 type_width=max_col_types)
        else:
            null_count = [i[2] for i in column_names_and_types]
            max_null_count = len(str(max(null_count, key=len)))
            for colname, coltype, num_nulls in column_names_and_types:
                dtypes_string += "{0: <{name_width}}{1: <{count_width}} non-null {2: <{type_width}}\n".format(colname,
                                                                                                              num_nulls,
                                                                                                              coltype,
                                                                                                              name_width=max_col_names,
                                                                                                              count_width=max_null_count,
                                                                                                              type_width=max_col_types)
        # Remove last new line character.
        dtypes_string = dtypes_string[:-1]
        return dtypes_string

    @staticmethod
    def _get_metadata_from_table(table_name):
        """
        Retrieves column metadata by executing a HELP COLUMN command.

        PARAMETERS:
            table_name - The table name or view name.

        RETURNS:
            returns the result set (column information) from HELP COLUMN.

        RAISES:
            Database error if an error occurred while executing the HELP COLUMN.

        EXAMPLES:
            df = DataFrame.from_table('mytab')
            metadata = _get_metadata_from_table(df._table_name)
        """
        # Construct HELP COLUMN command.
        help_col_sql = SQLBundle._build_help_column(table_name)
        # Execute HELP COLUMN command.
        return UtilFuncs._execute_query(help_col_sql)

    @staticmethod
    def _extract_select_string(select_expression):
        """
        Takes in a string/list representing a Pandas selection clause of any of the forms (only):
            a) "col1" or 'col1'
            b) ["col 1"] or ['col 1']
            c) ["col1", "col2", "col3"] or ['col1', 'col2', 'col3']
            d) [['col1', 'col2', 'col3']] or [["col1", "col2", "col3"]]

        And returns a list with column strings representing the selection of the form:
            a)  ['col1']
            b)  ['col 1']
            c)  ['col1','col2','col3']
            d)  ['col1','col2','col3']

        Column Names ("col1", "col2"..) are Strings representing database table Columns.
        All Standard Teradata Data-Types for columns supported: INTEGER, VARCHAR(5), FLOAT.

        PARAMETERS:
            selection_expression -  Expression representing column selection
            Type - String or List of Strings or List of List (Single level only)
            Required - Yes

        EXAMPLES:
            UtilFuncs._extract_select_string([['col1', 'col2']])
            UtilFuncs._extract_select_string("col1")
            UtilFuncs._extract_select_string(["col1"])
            UtilFuncs._extract_select_string(["col1","col2","col3"])

        RETURNS:
            List of Strings representing column names.

        RAISES:
            TeradataMlException
        """
        column_list = []

        # Single String column
        if isinstance(select_expression, str):
            # Error handling - Empty String
            if select_expression ==  "":
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_NONE_OR_EMPTY),
                                      MessageCodes.TDMLDF_SELECT_NONE_OR_EMPTY)
            else:
                column_list.append(UtilFuncs._teradata_quote_arg(select_expression.replace("'", "").replace('"', '').strip(), "\""))

        # Error Handling -  [],  [""], [None], ["None"], ['col1', None], ['col1', '']
        elif isinstance(select_expression, list) and (len(select_expression) ==  0  or
                                                    any(element in [None, "None", ""] for element in select_expression)):
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_NONE_OR_EMPTY),
                                      MessageCodes.TDMLDF_SELECT_NONE_OR_EMPTY)

        # List - ["col1"] or ["col1", "col2", "col3"]
        elif isinstance(select_expression, list) and all(isinstance(element, str) for element in select_expression):
            if len(select_expression) == 1:
                column_list.append(UtilFuncs._teradata_quote_arg(select_expression[0].replace("'", "").replace('"', '').strip(), "\""))
            else:
                column_list = [UtilFuncs._teradata_quote_arg(element.replace("'","").replace('"', '').strip(), "\"") for element in select_expression]

        # List of List (Single level only - Pandas Syntax) - [["col1", "col2", "col3"]]
        elif isinstance(select_expression, list) and isinstance(select_expression[0], list):
            # Error Handling - [[]], [[""]], [[None]], [['col1', None]], [['col1', "None"]], ["col1", ""]
            if len(select_expression[0]) ==  0  or any(element in [None, "None", ""] for element in select_expression[0]):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_NONE_OR_EMPTY),
                                      MessageCodes.TDMLDF_SELECT_NONE_OR_EMPTY)

            else:
                column_list = [UtilFuncs._teradata_quote_arg(element.replace("'","").replace('"', '').strip(), "\"") for element in select_expression[0]]

        # Any other Format - Raise Format Exception
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_SELECT_INVALID_FORMAT),
                                      MessageCodes.TDMLDF_SELECT_INVALID_FORMAT)
        return column_list

    @staticmethod
    def _get_primary_index_from_table(table_name):
        """
        Retrieves the primary index by executing a HELP INDEX command.
        PARAMETERS:
            table_name - The table name or volatile table name.
        RETURNS:
            Returns a list containing the primary index columns from HELP INDEX.
            If the there are no primary index (NoPI table), then returns None.
        RAISES:
            Database error if an error occurred while executing the HELP INDEX.
        EXAMPLES:
            df = DataFrame.from_table('mytab')
            index_labels = df._get_metadata_from_table(df._table_name)
        """
        # Construct HELP INDEX command.
        help_index_sql = SQLBundle._build_help_index(table_name)

        # Execute HELP COLUMN command.
        rows = UtilFuncs._execute_query(help_index_sql)
        index_labels = []
        for row in rows:
            if row[1].rstrip() == 'P':
                if("," in row[2]):
                    index_labels.extend(row[2].split(','))
                else:
                    index_labels.append(row[2])
        if len(index_labels) > 0:
            return index_labels
        else:
            return None

    @staticmethod
    def _validate_sort_col_type(sort_col_type, sort_col_values):
        """
        Validates a list of sort column values with the sort column type.

        PARAMETERS:
            sort_col_type - The sort column type.
            sort_col_values - A single value or list-like values

        RETURNS:

        RAISES:
            TeradataMlException

        EXAMPLES:
            df_utils._validate_sort_col_type(PythonTypes.PY_STRING_TYPE, ["Jan", "Feb"])
            df_utils._validate_sort_col_type(PythonTypes.PY_STRING_TYPE, "Jan")
            df_utils._validate_sort_col_type(PythonTypes.PY_INT_TYPE, [1, 2])
        """
        if isinstance(sort_col_values, list):
            if sort_col_type == PythonTypes.PY_STRING_TYPE:
                if not all(isinstance(i, str) for i in sort_col_values):
                    msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE).format(sort_col_type)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE)
            else: # numeric type
                if not all(isinstance(i, numbers.Integral) for i in sort_col_values):
                    msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE).format(sort_col_type)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE)
        elif isinstance(sort_col_values, (tuple, dict)):
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_DROP_ARGS), MessageCodes.TDMLDF_DROP_ARGS)
        else:
            if sort_col_type == PythonTypes.PY_STRING_TYPE:
                if not isinstance(sort_col_values, str):
                    msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE).format(sort_col_type)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE)
            else: # numeric type
                if not isinstance(sort_col_values, numbers.Integral):
                    msg = Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE).format(sort_col_type)
                    raise TeradataMlException(msg, MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE)

    @staticmethod
    def _get_pandas_dataframe(table_name, index_column, df_index_label, num_rows, orderby = None):
        """
        Returns a Pandas DataFrame using the specified Parameters.
        Uses a) User specified Index column(s), if specified.
             b) Otherwise, TeradataML DataFrame object _index_label column, when set.
             c) Otherwise, Primary Index retrieved via DB Table, if exists.
             d) Otherwise, No index_column used (default Pandas integer index returned)

        PARAMETERS:
            table_name - String representing TDML DF object _table_name (generated for unexecuted nodes).
            index_column - User specified column(s) to use as Pandas Index. String/List of strings.
            df_index_label - String representing TDML DF object _index_label.
            num_rows - Integer representing Number of rows used to create Pandas DF.

        EXAMPLES:
             _get_pandas_dataframe(table_name = 'df_admissions_train', index_column = 'id',
                                   num_rows = 100)

        RETURNS:
            Pandas DataFrame when valid parameters used.
            Otherwise, None.

        """
        # Generate SQL Query using Table name & number of rows required.
        read_query = SQLBundle._build_top_n_print_query(table_name, num_rows, orderby)
        con = get_context()
        index_col = None

        # Index Order: 1) User specified 2) TDMLDF index 3) DB PI 4)Else default integer index
        if index_column:
            index_col = index_column
        elif df_index_label:
            index_col = df_index_label
        else:
            try:
                index_col = DataFrameUtils._get_primary_index_from_table(table_name)
            except Exception as err:
                index_col = None

        # Use index_col when exists, else default integer index (no index_col)
        if index_col is not None:
            pandas_df = pd.read_sql_query(read_query, con, index_col = index_col, coerce_float = False)
        else:
            pandas_df = pd.read_sql_query(read_query, con, coerce_float = False)

        return pandas_df

    def _get_required_columns_types_from_metaexpr(metaexpr, col_list = None):
        """
        Retrieves column names and types from meta expression. If you want to get types for only some columns,
        pass those columns to 'col_list' argument.

        PARAMETERS:
           metaexpr - Meta expression from which columns and types to be retrieved.
           col_list - Column list for which you want to get types

        RETURNS:
           Dictionary: key as column name and datatype as value.

        EXAMPLES:
           df = DataFrame.from_table('mytab')
           metadata = _get_required_columns_types_from_metaexpr()
        """

        if isinstance(col_list, str):
            col_list = [col_list]

        if col_list is not None and not isinstance(col_list, list):
            return None

        meta_cols = metaexpr.t.c
        meta_columns = [c.name for c in meta_cols]
        col_names = []
        col_types = []
        for col_name in meta_columns:
            if col_list is None or DataFrameUtils._check_column_exists(col_name, col_list):
                col_names.append(meta_cols[col_name].name)
                col_types.append(meta_cols[col_name].type)

        return dict(zip(col_names, col_types))

    @staticmethod
    def _check_column_exists(column_name, df_columns):
        """
         Checks provide column present in list of columns or not.

         PARAMETERS:
            column_name - Column name which need to be check.
            df_columns  - List columns in which column to be check.

         RETURNS:
            True if column exists otherwase False.

         EXAMPLES:
            df = DataFrame.from_table('mytab')
            metadata = _check_column_exists("col1", df.columns)
        """
        unquoted_df_columns = [column.replace('"', "") for column in df_columns]
        if column_name.replace('"', "") in unquoted_df_columns:
            return True
        else:
            return False

    @staticmethod
    def _validate_agg_function(func, col_names):
        """
        Internal function to validate column names against actual
        column names passed as parameter and aggregate operations
        against valid aggregate operations.

        PARAMETERS:
            func  - (Required) Specifies the function(s) to be
                    applied on TeradataML DataFrame columns.
                    Acceptable formats for function(s) are string,
                    dictionary or list of strings/functions.
                    Accepted combinations are:
                    1. String function name
                    2. List of string functions
                    3. Dictionary of column names -> string function
                       (or list of string functions)
            col_names - List. Names of the columns in Dataframe.

        RETURNS:
            operations - dict of columns -> aggregate operations
            Unified dictionary, similar to func, even for string and
            list of strings or functions.

        RAISES:
            1. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'func' is/are
                invalid.

                Possible Value :
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            2. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in 'func' is not present in the dataframe.

                Possible Value :
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

        EXAMPLES:
            Let the dataframe contain 2 columns, col1 and col2.

            VALID EXAMPLES:
            1. operations = DataFrameUtils._validate_agg_function(
                    operation = 'mean', ['col1', 'col2'])

            2. operations = DataFrameUtils._validate_agg_function(
                    operation = ['mean', 'min'], ['col1', 'col2'])

            3. operations = DataFrameUtils._validate_agg_function(
                    {'col1' : ['mean', 'min'], 'col2' : 'count'},
                                                    ['col1', 'col2'])

            INVALID EXAMPLES:
            1. operations = DataFrameUtils._validate_agg_function(
                    operation = 'counter', ['col1', 'col2'])

            2. operations = DataFrameUtils._validate_agg_function(
                    {'col1' : ['mean', 'min'], 'col55' : 'count'},
                                                    ['col1', 'col2'])
        """
        operations = {}

        valid_aggregate_operations = UtilFuncs._get_valid_aggregate_operations()

        if isinstance(func, str):
            for column in col_names:
                operations[column] = [func]
        elif isinstance(func, list):
            for column in col_names:
                operations[column] = func
        else:
            for column in func:
                if isinstance(func[column], str):
                    func[column] = [func[column]] # Converts string inside dict to list
            operations = func

        given_columns = operations.keys()
        invalid_columns = []
        all_operations = []
        for col in given_columns:
            all_operations.extend(operations[col])
            if col not in col_names:
                invalid_columns.append(col)
        if len(invalid_columns) > 0:  # If any of the columns specified is not present in dataframe
            col_names.sort()
            invalid_columns.sort()
            msg = Messages.get_message(MessageCodes.TDMLDF_AGGREGATE_INVALID_COLUMN). \
                format(", ".join(invalid_columns), 'func', ", ".join(col_names))
            raise TeradataMlException(msg, MessageCodes.TDMLDF_AGGREGATE_INVALID_COLUMN)

        all_operations = list(set(all_operations))
        invalid_aggregates = []
        for operation in all_operations:
            if operation not in valid_aggregate_operations:
                invalid_aggregates.append(operation)
        if len(invalid_aggregates) > 0: # If any of the aggregate operations specified is not valid
            valid_aggregate_operations.sort()
            invalid_aggregates.sort()
            msg = Messages.get_message(MessageCodes.TDMLDF_INVALID_AGGREGATE_OPERATION). \
                format(", ".join(invalid_aggregates), ", ".join(valid_aggregate_operations))
            raise TeradataMlException(msg, MessageCodes.TDMLDF_INVALID_AGGREGATE_OPERATION)

        return operations

    @staticmethod
    def _construct_sql_expression_for_aggregations(column_names, column_types, func):
        """
        Internal function to create and return the sql expression
        corresponding to given operation, given column_names and
        column_types.

        Column_types are used to check whether all the datatypes are
        valid types for given operation and throw exception if they
        are not.

        PARAMETERS :
            column_names -  List. Names of the columns in Dataframe
            column_types -  List. List of sqlachemy_teradata.types of
                            the corresponding columns of Dataframe
            func         -  Specifies the function(s) to be applied on
                            TeradataML DataFrame columns.Acceptable
                            formats for function(s) are string,
                            dictionary or list of strings/functions.
                            Accepted combinations are:
                            1. String function name
                            2. List of functions
                            3. Dictionary containing column name as
                               key and aggregate function name (string
                               or list of strings) as value

            All parameters are required.

        RETURNS :
            a)sql expression as
                1. 'min(col1) as min_col1, min(col2) as min_col2' if
                        col1 and col2 are the columns in Dataframe and
                        operation is 'min'
                2. 'max(col1) as max_col1, max(col2) as max_col2' if
                        col1 and col2 are the columns in Dataframe and
                        operation is 'max'
                3. 'min(col1) as min_col1, stddev_samp(col2) as
                        std_col2' if col1, col2 are the columns in
                        Dataframe and operations are min, std.
                etc...
            b) new columns' names (eg min_col1, min_col2 ...)
            c) new columns' types
        RAISES:
            TeradataMLException
            1. TDMLDF_AGGREGATE_COMBINED_ERR - If the provided
                aggregate operations do not support specified columns.

                Possible Value :
                No results. Below is/are the error message(s):
                All selected columns [(col1 - VARCHAR)] is/are
                unsupported for 'sum' operation.

            2. TDMLDF_INVALID_AGGREGATE_OPERATION - If the aggregate
                operation(s) received in parameter 'func' is/are
                invalid.

                Possible Value :
                Invalid aggregate operation(s): minimum, counter.
                Valid aggregate operation(s): count, max, mean, min,
                std, sum.

            3. TDMLDF_AGGREGATE_INVALID_COLUMN - If any of the columns
                specified in func is not present in the dataframe.

                Possible Value :
                Invalid column(s) given in parameter func: col1.
                Valid column(s) : A, B, C, D.

        EXAMPLES:
            col_names, col_types = \
            df_utils._get_column_names_and_types_from_metaexpr(
                                                     self._metaexpr)
            expr, new_col_names, new_col_types = \
            df_utils._construct_sql_expression_for_aggregations(
                                    col_names, col_types, 'min')

            expr1, new_col_names1, new_col_types1 = \
            df_utils._construct_sql_expression_for_aggregations(
                                col_names, col_types, ['min', 'sum'])

            expr2, new_col_names2, new_col_types2 = \
            df_utils._construct_sql_expression_for_aggregations(
                    col_names, col_types, {'col1 : ['min', 'sum'],
                                                'col2' : 'mean'})

        """

        # eg of column_types: [VARCHAR(length=13), INTEGER(), VARCHAR(length=60), VARCHAR(length=5),
        # FLOAT(precision=0)]

        # eg of types of each column are <class 'teradatasqlalchemy.types.VARCHAR'>,
        # <class 'teradatasqlalchemy.types.INTEGER'>, <class 'teradatasqlalchemy.types.FLOAT'>,
        # <class 'teradatasqlalchemy.types.INTERVAL_MINUTE_TO_SECOND'> etc..


        # 'operations' contains dict of columns -> list of aggregate operations
        operations = DataFrameUtils._validate_agg_function(func, column_names)

        col_names_and_types = dict(zip(column_names, column_types))

        all_valid_columns = []
        all_invalid_columns = {}
        all_new_column_names = []
        all_new_column_types = []

        column_supported = {}   # For each column, the value is True if there is at least one
                                # valid operation (operation on valid datatype)

        tdp = preparer(td_dialect)

        for column in operations:
            column_supported[column] = False
            valid_columns = []
            invalid_columns = {}
            new_column_names = []
            new_column_types = []
            for operation in operations[column]:
                column_type = col_names_and_types[column]

                if type(column_type) in \
                        UtilFuncs._get_unsupported_data_types_for_aggregate_operations(operation):
                    if operation in invalid_columns:
                        invalid_columns[operation].append("({0} - {1})".format(column, column_type))
                    else:
                        invalid_columns[operation] = ["({0} - {1})".format(column, column_type)]
                else:
                    column_supported[column] = True
                    td_operation = operation
                    if operation == 'mean':
                        td_operation = 'avg'
                    if operation == 'std':
                        td_operation = 'stddev_samp'

                    # Quoting column names used in generating query
                    quoted_parent_column_name = tdp.quote("{0}".format(column))
                    quoted_new_column_name = tdp.quote("{1}_{0}".format(column, operation))

                    valid_columns.append('{2}({0}) as {1}'.format(quoted_parent_column_name,
                                                quoted_new_column_name, td_operation))

                    new_column_names.append("{1}_{0}".format(column, operation))

                    # For mean and std operation, all numeric-type datatypes are converted to FLOAT
                    # datatype
                    uf = UtilFuncs()
                    if operation in ['mean', 'std'] and column_type in \
                            uf._get_numeric_datatypes():
                        new_column_types.append(FLOAT())
                    elif operation == 'count':  # By default, type of all Count(column) is Integer
                        new_column_types.append(INTEGER())
                    else:
                        new_column_types.append(column_type)

            all_valid_columns.extend(valid_columns)
            all_new_column_names.extend(new_column_names)
            all_new_column_types.extend(new_column_types)

            for operation in invalid_columns:
                if operation in all_invalid_columns:
                    all_invalid_columns[operation].extend(invalid_columns[operation])
                else:
                    all_invalid_columns[operation] = invalid_columns[operation]

        unsupported_columns = [col for col in column_supported if column_supported[col] == False]

        error_msgs = []
        for operation in sorted(all_invalid_columns):
            all_invalid_columns[operation].sort()   # helps in catching the columns in
                                                    # lexicographic order
            error = MessageCodes.TDMLDF_AGGREGATE_UNSUPPORTED.value.format(
                ", ".join(all_invalid_columns[operation]), operation)
            error_msgs.append(error)

        if not isinstance(func, str) and not all(column_supported[oper] for oper in
                                                column_supported):
            new_msg = MessageCodes.TDMLDF_AGGREGATE_AGG_DICT_ERR.value.format(
                                                                    ", ".join(unsupported_columns))
            error_msgs.append(new_msg)
            msg = Messages.get_message(MessageCodes.TDMLDF_AGGREGATE_COMBINED_ERR).\
                                                                format("\n".join(error_msgs))
            raise TeradataMlException(msg, MessageCodes.TDMLDF_AGGREGATE_COMBINED_ERR)

        elif len(all_valid_columns) == 0:  # No supported columns in the given list of columns
            raise TeradataMlException(Messages.get_message(
                MessageCodes.TDMLDF_AGGREGATE_COMBINED_ERR).format("\n".join(error_msgs)),
                                      MessageCodes.TDMLDF_AGGREGATE_COMBINED_ERR)

        aggregate_expr = ", ".join(all_valid_columns)
        return aggregate_expr, all_new_column_names, all_new_column_types

    @staticmethod
    def _get_column_names_and_types_from_metaexpr(metaexpr):
        """
        Internal function to return column names and respective types
        given _metaexpr.

        PARAMETERS:
            metaexpr - Dataframe's metaexpr. It is used to get column
                       names and types

        RETURNS:
            Two lists - one for column names and another for
                        column types

        RAISES:
            None

        EXAMPLES:
            dfUtils._get_column_names_and_types_from_metaexpr(
                                                    df._metaexpr)
        """

        # Constructing New Column names & Types for selected columns ONLY using Parent _metaexpr
        col_names = [c.name for c in metaexpr.c]
        col_types = [c.type for c in metaexpr.c]
        return col_names, col_types

    @staticmethod
    def _insert_all_from_table(to_table_name, from_table_name, column_list):
        """
        Inserts all records from one table into the second, using columns ordered by column list.

        PARAMETERS:
            to_table_name - String specifying name of the SQL Table to insert to.
            insert_from_table_name - String specifying name of the SQL Table to insert from.
            column_list - List of strings specifying column names used in the insertion.

        RETURNS:
            None

        RAISES:
            Database error if an error occurred while executing the insert command.

        EXAMPLES:
            df_utils._insert_all_from_table('table1_name', 'table2_name', ['col1', 'col2', 'col3'])
        """
        # Construct INSERT command.
        column_order_string = ', '.join(column_list)
        full_to_table_name = _get_current_databasename() + "." + to_table_name
        insert_sql = SQLBundle._build_insert_from_table_query(full_to_table_name, from_table_name, column_order_string)

        # Execute INSERT command.
        return UtilFuncs._execute_ddl_statement(insert_sql)

    @staticmethod
    def _dataframe_has_column(data, column):
        """
        Function to check whether column names in columns are present in given dataframe or not.
        This function is used currently only for Analytics wrappers.

        PARAMETERS:
            data - TeradataML DataFrame to check against for column existence.
            column - Column name (a string).

        RAISES:
            None

        EXAMPLES:
            DataFrameUtils._dataframe_has_column(data, col)
        """
        if column in [c.name for c in data._metaexpr.c]:
            return True

        return False

    @staticmethod
    def _validate_to_pandas_parameters(df, index_column, num_rows):
        """
        Validates the to_pandas API parameters.

        PARAMETERS:
            df - TeradataML DataFrame object used to extract column information.
            index_column - User Specified String/List specifying columns to use as Pandas Index.
            num_rows - Integer specifying number of rows to use to create Pandas Dataframe;

        EXAMPLES:
             _validate_to_pandas_parameters(index_column, num_rows)

        RETURNS:
            None

        RAISES:
            TeradataMlException (TDMLDF_INFO_ERROR, UNSUPPORTED_DATATYPE,
                                 INVALID_ARG_VALUE, DF_LABEL_MISMATCH)
        """

        if df._metaexpr is not None:
            df_column_list = [col.name for col in df._metaexpr.c]
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_INFO_ERROR),
                                      MessageCodes.TDMLDF_INFO_ERROR)

        if index_column is not None:
            # Check Format validity for index_column
            if not (isinstance(index_column, str) or isinstance(index_column, list)):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "index_column",
                                                               "string or list of strings"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            DataFrameUtils._check_column_in_dataframe(df, index_column, 'index_column')

        # Check if TDML DF has appropriate index_label set when required
        df_index_label = df._index_label

        if df_index_label is not None:
            if isinstance(df_index_label, str):
                if df_index_label not in df_column_list:
                    raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)
            elif isinstance(df_index_label, list):
                for index_label in df_index_label:
                    if index_label not in df_column_list:
                        raise TeradataMlException(Messages.get_message(MessageCodes.DF_LABEL_MISMATCH), MessageCodes.DF_LABEL_MISMATCH)

        # Check Format validity for num_rows
        if num_rows is not None:
            if not isinstance(num_rows, int):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "num_rows", "int"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)
            elif num_rows <= 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,num_rows, "num_rows",
                                                               "integer value greater than zero"),
                                          MessageCodes.INVALID_ARG_VALUE)

    def _check_column_in_dataframe(df, column_names, error_message_arg = 'Dataframe column name'):
        """
        Internal Utility function to check if given column(s) (String or list of strings)
        exists in the Dataframe columns or not.

        PARAMETERS:
            df - TeradataML DataFrame object used to extract column information.
            column_names - String or List of strings specifying column names to be checked.

            error_message_arg (optional) - Specifies column name/argument to be used in the
                exception message of the format: "Invalid value passed for argument: error_message_arg"
                Default: 'Dataframe column name'

        RETURNS:
            True, when all columns specified are valid (exist in DataFrame)
            TeradataMlException, otherwise.

        RAISES:
            TeradataMlException (INVALID_ARG_VALUE)

        EXAMPLES:
            _check_column_in_dataframe(df, 'column_name')
            _check_column_in_dataframe(df, ['column_name1', 'column_name2'])
            _check_column_in_dataframe(df, 'column_name', error_message_arg = 'index_column')

        """
        if df._metaexpr is not None:
            df_column_list = [col.name for col in df._metaexpr.c]

        if isinstance(column_names, list):
            for column in column_names:
                #if not isinstance(column, str) or (column not in df_column_list):
                if not isinstance(column, str) or not DataFrameUtils._check_column_exists(column, df_column_list):
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND,column,""),
                                          MessageCodes.TDMLDF_COLUMN_NOT_FOUND)

        elif isinstance(column_names, str):
            #if column_names not in df_column_list:
            if not DataFrameUtils._check_column_exists(column_names, df_column_list):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_COLUMN_NOT_FOUND, column_names, ""),
                                          MessageCodes.TDMLDF_COLUMN_NOT_FOUND)
        return True
