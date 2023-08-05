#!/usr/bin/python
# ##################################################################
#
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# ##################################################################

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.context.context import *
import sqlalchemy

from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, Unicode, String, Float, Boolean, DateTime, Interval, BigInteger, Time

from teradatasqlalchemy.compiler import TDCreateTablePost as post
from sqlalchemy.sql.expression import insert

import pandas as pd
import numpy as np
from teradataml.common.utils import UtilFuncs
from teradataml.dataframe.dataframe import *
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
import teradataml

def copy_to_sql(df, table_name, schema_name=None, if_exists='append', index=False, index_label=None,
            primary_index=None, temporary=False):
    """
    Writes records stored in a Pandas DataFrame or a TeradataML DataFrame to a Teradata database.

    PARAMETERS:

        df (required) : The Pandas or TeradataML DataFrame object to be saved.
             Type: pandas.DataFrame or teradataml.dataframe.dataframe.DataFrame

        table_name (required) : Specifies the name of the table to be created in the database.
            Type : String

        schema_name (optional): Specifies the name of the SQL schema in the database to write to.
            Type: String
            Default: None (Uses default database schema).

        if_exists (optional): Specifies the action to take when table already exists in the database.
            Type : String; possible values: {'fail', 'replace', 'append'}
                - fail: If table exists, do nothing.
                - replace: If table exists, drop it, recreate it, and insert data.
                - append: If table exists, insert data. Create if does not exist.
            Default : append

        index (optional): Specifies whether to save Pandas DataFrame index as a column or not.
            Type : Boolean (True or False)
            Default : False
            Only use as True when attempting to save Pandas DataFrames (and not on TeradataML DataFrames).

        index_label (optional): Column label for Pandas DataFrame index column(s).
            Type : String
            Default : None
            If None is given (default) and `index` is True, then a default label 'index_label' is used.
            Only use as True when attempting to save Pandas DataFrames (and not on TeradataML DataFrames).

        primary_index (optional): Creates Teradata Table(s) with Primary index column when specified.
            Type : String or List of strings
                Example:
                    primary_index = 'my_primary_index'
                    primary_index = ['my_primary_index1', 'my_primary_index2', 'my_primary_index3']
            Default : None
            For Pandas DataFrames, when None, default primary index is selected as per Teradata table creation rules.
            For TeradataML DataFrames, when None, No Primary Index Teradata tables are created and saved to.

        temporary (optional): Creates Teradata SQL tables as permanent or volatile.
            Type : Boolean (True or False)
            Default : False
            When True, volatile Tables are created.
            When False, permanent tables are created.

    RETURNS:
        None

    RAISES:
        TeradataMlException

    EXAMPLES:
        1. Saving a Pandas DataFrame:

            from teradataml.dataframe.copy_to import copy_to_sql

            df = {'emp_name': ['A1', 'A2', 'A3', 'A4'],
            'emp_sage': [100, 200, 300, 400],
            'emp_id': [133, 144, 155, 177],
            'marks': [99.99, 97.32, 94.67, 91.00]
            }

            pandas_df = pd.DataFrame(df)

            a) Save a Pandas DataFrame using a dataframe & table name only:
            copy_to_sql(df = pandas_df, table_name = 'my_table_name')

            b) Save a Pandas DataFrame by specifying additional parameters:
            copy_to_sql(df = my_df, table_name = 'my_table_name', schema_name = 'default_schema',
                        index = True, index_label = 'my_index_label', temporary = False,
                        primary_index = ['my_primary_index'], if_exists = 'append')

        2. Saving a TeradataML DataFrame:

            from teradataml.dataframe.dataframe import DataFrame
            from teradataml.dataframe.copy_to import copy_to_sql

            df = DataFrame('test_table_name')
            df2 = df1.select(['col_name1', 'col_name2'])

            a) Save a TeradataML DataFrame by using only a table name:
            df2.to_sql('my_table_name2')

            b) Save a TeradataML DataFrame by using additional parameters:
            df2.to_sql(table_name = 'my_table_name2', if_exists='append',
                       primary_index = ['my_primary_index'], temporary=False, schema_name='my_schema_name')

            c) Alternatively, Save a TeradataML DataFrame by using copy_to_sql:
            copy_to_sql(df2, 'my_table_name2')

            d) Save a TeradataML DataFrame by using copy_to_sql with additional parameters:
            copy_to_sql(df = df2, table_name = 'my_table_name2', schema_name = 'default_schema',
                    temporary = False, primary_index = None, if_exists = 'append')
    """
    #Deriving global connection using context.get_context()
    con = get_context()

    try:
        if con is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE)

        # df is a Pandas DataFrame object
        if isinstance(df, pd.DataFrame):

            # Validate DataFrame & related flags; Proceed only when True
            _validate_copy_parameters(df, table_name, index, index_label, primary_index, temporary, if_exists, schema_name)

            # Default behavior - Using pandas to_sql to save to database
            if primary_index is None and not temporary and index is False:
                # For Pandas object types, create dtype dictionary with mapping to SqlAlchemy String type (overwrite CLOB's)
                dtype_dict = {}
                df_string_cols_only = df.select_dtypes(include = [np.object])
                df_string_cols, df_string_types = _extract_column_info(df_string_cols_only)
                for col_index in range(0, len(df_string_cols)):
                    dtype_dict[df_string_cols[col_index]] = df_string_types[col_index]

                df.to_sql(table_name, con, if_exists=if_exists, index=index, index_label=index_label, schema=schema_name, dtype = dtype_dict)

            # All other cases - Requires Special Table creation - using helper function
            else:
                table_exists = con.dialect.has_table(con, table_name)
                if not table_exists or (table_exists and if_exists == 'replace'):

                    if table_exists:
                        UtilFuncs._drop_table(table_name)

                    table = _create_table_object(df, table_name, con, primary_index, temporary, if_exists,
                                                 index, index_label, schema_name)

                    if table is not None:
                        table.create()
                    else:
                        raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_OBJECT_CREATION_FAILED),
                                                  MessageCodes.TABLE_OBJECT_CREATION_FAILED)

                    # Support for saving Pandas index/Volatile tables doesn't exist - Manually inserting (batch) rows for now
                    if index is True or temporary is True:
                        _insert_from_dataframe(df, con, table, index, index_label)
                    # When index isn't saved & for permanent tables, to_sql insertion used (batch)
                    else:
                        _insert_data(df, table_name, con, index, index_label)

                elif table_exists and if_exists == 'append':
                    meta = sqlalchemy.MetaData(con)
                    table = Table(table_name, meta, autoload=True, autoload_with=con)

                    if table is not None:
                        _insert_from_dataframe(df, con, table, index, index_label)

                elif table_exists and if_exists == 'fail':
                    raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_ALREADY_EXISTS, table_name),
                                              MessageCodes.TABLE_ALREADY_EXISTS)

        # df is a TeradataML DataFrame object (to_sql wrapper used)
        elif isinstance(df, teradataml.dataframe.dataframe.DataFrame):

            # Un-executed - Generate/Execute Nodes & Set Table Name
            if df._table_name is None:
                if df._nodeid:
                    df._table_name = df_utils._execute_node_return_db_object_name(df._nodeid)
                else:
                    raise TeradataMlException(Messages.get_message(MessageCodes.COPY_TO_SQL_FAIL),
                                              MessageCodes.COPY_TO_SQL_FAIL)

            # Validate parameters; proceed only if parameters are valid.
            _validate_copy_parameters(df, table_name, index, index_label, primary_index, temporary, if_exists, schema_name)

            # Handle cases for table already exists & append/replace/fail
            table_exists = con.dialect.has_table(con, table_name)
            df_column_list = [col.name for col in df._metaexpr.c]

            if not table_exists or (table_exists and if_exists == 'replace'):

                if table_exists:
                    UtilFuncs._drop_table(table_name)

                table = _create_table_object_from_tdmldf(df, table_name, con, primary_index, temporary, schema_name)

                if table is not None:
                    table.create()
                    df_utils._insert_all_from_table(table_name, df._table_name, df_column_list)
                else:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_OBJECT_CREATION_FAILED),
                                              MessageCodes.TABLE_OBJECT_CREATION_FAILED)

            elif table_exists and if_exists == 'append':
                meta = sqlalchemy.MetaData(con)
                table = Table(table_name, meta, autoload=True, autoload_with=con)

                if table is not None:
                    cols_compatible = _check_columns_insertion_compatible(table.c, df._metaexpr.t.c)

                    if cols_compatible:
                        df_utils._insert_all_from_table(table_name, df._table_name, df_column_list)
                    else:
                        raise TeradataMlException(Messages.get_message(MessageCodes.INSERTION_INCOMPATIBLE),
                                                  MessageCodes.INSERTION_INCOMPATIBLE)

            elif table_exists and if_exists == 'fail':
                    raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_ALREADY_EXISTS, table_name),
                                              MessageCodes.TABLE_ALREADY_EXISTS)

    except TeradataMlException:
        raise
    except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.COPY_TO_SQL_FAIL), MessageCodes.COPY_TO_SQL_FAIL) from err


def _validate_copy_parameters(df, table_name, index, index_label, primary_index, temporary, if_exists, schema_name):
    """
    This is an internal function used to validate the copy request.
    Dataframe, connection & related parameters are checked.
    Saving to database is proceeded to only when validation returns True.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

        table_name : Name of SQL table.

        index : Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label : Column label for index column(s).

        primary_index : Creates Teradata Table(s) with Primary index column if specified.

        temporary : Flag specifying whether SQL table to be created is Volatile or not.

        if_exists : String specifying action when table already exists in SQL Schema.

        schema_name: Name of the SQL Database.

    RETURNS:
        True, when all parameters are valid.

    RAISES:
        TeradataMlException, when parameter validation fails.

    EXAMPLES:
        _validate_copy_parameters(df = my_df, table_name = 'test_table', index = True, index_label = None,
                                  primary_index = None, temporary = True, if_exists = 'replace')
    """
    if df is None or _check_dataframe(df) is False:
        raise TeradataMlException(Messages.get_message(MessageCodes.IS_NOT_VALID_DF),
                                  MessageCodes.IS_NOT_VALID_DF)

    else:
        if isinstance(df, pd.DataFrame):
            df_columns = df.columns.get_values().tolist()
        else:
            df_columns = [col.name for col in df._metaexpr.c]

        # TODO: Replace hard-coded check with TeradataConstants constant when PR #73 Merged
        if len(df.columns) > 2048:
            raise TeradataMlException(Messages.get_message(MessageCodes.TD_MAX_COL_MESSAGE),
                                      MessageCodes.TD_MAX_COL_MESSAGE)

        if table_name is not None and not isinstance(table_name, str):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "table_name", "String or List of strings"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

        if table_name in ('', None):
            raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, 'table_name'),
                                          MessageCodes.ARG_EMPTY)

        if primary_index and (not (isinstance(primary_index, str) or isinstance(primary_index, list))):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "primary_index", "String or List of strings"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

        if primary_index is not None and primary_index not in df_columns:
            if isinstance(primary_index, list):
                for column in primary_index:
                    if column not in df_columns:
                        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_PRIMARY_INDEX),
                                                  MessageCodes.INVALID_PRIMARY_INDEX)
            else:
                if len(primary_index.strip()) == 0:
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, 'primary_index'),
                                              MessageCodes.ARG_EMPTY)
                else:
                    raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_PRIMARY_INDEX),
                                          MessageCodes.INVALID_PRIMARY_INDEX)

        if schema_name is not None and not isinstance(schema_name, str):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "schema_name", "String"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

        if schema_name is not None and len(schema_name.strip()) == 0:
            raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, 'schema_name'),
                                      MessageCodes.ARG_EMPTY)

        if not isinstance(index, bool):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "index", "Boolean (True/False)"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

        if not isinstance(temporary, bool):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "temporary", "Boolean (True/False)"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

        if if_exists not in ('append', 'replace', 'fail'):
            raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                          str(if_exists), 'if_exists', 'append, replace, fail'),
                                          MessageCodes.INVALID_ARG_VALUE)

        if isinstance(df, pd.DataFrame):
            if index_label is not None and not isinstance(index_label, str):
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, "index_label", "String"),
                                          MessageCodes.UNSUPPORTED_DATATYPE)

            if index_label is not None and len(index_label.strip()) == 0:
                raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, 'index_label'),
                                          MessageCodes.ARG_EMPTY)

            if index is True and index_label in df_columns:
                raise TeradataMlException(Messages.get_message(MessageCodes.INDEX_ALREADY_EXISTS), MessageCodes.INDEX_ALREADY_EXISTS)

            if index_label is not None and index is False:
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_INDEX_LABEL), MessageCodes.INVALID_INDEX_LABEL)

        elif isinstance(df, teradataml.dataframe.dataframe.DataFrame):
            # TeradataML DataFrame's do not support saving pandas index/index_label
            if index_label is not None:
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                          str(index_label), 'index_label', 'None'),
                                          MessageCodes.INVALID_ARG_VALUE)

            if index is not False:
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                          str(index), 'index', 'False'),
                                          MessageCodes.INVALID_ARG_VALUE)

def _create_table_object(df, table_name, con, primary_index, temporary, if_exists, index, index_label, schema_name):
    """
    This is an internal function used to construct a SQLAlchemy Table Object.
    This function checks appropriate flags and supports creation of Teradata
    specific Table constructs such as Volatile/Primary Index tables.


    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

        table_name : Name of SQL table.

        con : A SQLAlchemy connectable (engine/connection) object

        primary_index : Creates Teradata Table(s) with Primary index column if specified.

        temporary : Flag specifying whether SQL table to be created is Volatile or not.

        if_exists : String specifying action when table already exists in SQL Schema

        index : Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label : Column label for index column(s).

        schema_name : Specifies the name of the SQL schema in the database to write to.

    RETURNS:
        SQLAlchemy Table

    RAISES:
        N/A

    EXAMPLES:
        _create_table_object(df = my_df, table_name = 'test_table', con = tdconnection, primary_index = None,
                             temporary = True, if_exists = 'replace', index = True, index_label = None, schema_name = schema)
    """
    col_names, col_types = _extract_column_info(df)

    meta = MetaData()
    meta.bind = con

    # Dictionary to append special flags, can be extended to add Fallback, Journalling, Log etc.
    post_params = {}

    if temporary is True:
        post_params['on commit preserve rows'] = None

    pti = post(opts = post_params)

    if primary_index is not None and isinstance(primary_index, list):
        pti = pti.primary_index(unique=True, cols=primary_index)
    else:
        pti = pti.primary_index(unique=True, cols=[primary_index])

    # Create default Table construct with parameter dictionary
    if not index and not temporary:
        table = Table (table_name, meta,
                   *(Column(col_name, col_type)
                    for col_name, col_type in
                    zip(col_names, col_types)),
                    teradatasql_post_create = pti
                    )
    elif not index and temporary:
        table = Table (table_name, meta,
                   *(Column(col_name, col_type)
                    for col_name, col_type in
                    zip(col_names, col_types)),
                    teradatasql_post_create = pti,
                    prefixes=['VOLATILE']
                    )

    # Pandas Index needs to be saved - Create Table construct with added Index column
    else:
        index_name = df.index.name

        # Use index label if specified, else use Pandas DF Index name, else use default index_label ('index' is a keyword)
        if index_name in ('', None):
            index_name = index_label if index_label is not None else 'index_label'
            col_names.append(index_name)
            col_types.append(Integer)
        else:
            index_name = index_label if index_label is not None else index_name
            col_names.append(index_name)
            col_types.append(_get_sqlalchemy_mapping(df.index.dtype))

        # When Pandas Index is True, and PI is None, PI is Pandas index:
        if primary_index is None:
             pti = pti.primary_index(unique=True, cols=[index_name])

        # Create Table object with index appended to column names, types
        if temporary is False:
            table = Table (table_name, meta,
                       *(Column(col_name, col_type)
                        for col_name, col_type in
                        zip(col_names, col_types)),
                        teradatasql_post_create = pti
                        )
        else:
            table = Table (table_name, meta,
                       *(Column(col_name, col_type)
                        for col_name, col_type in
                        zip(col_names, col_types)),
                        teradatasql_post_create = pti,
                        prefixes=['VOLATILE']
                        )

    if schema_name is not None:
        table.schema = schema_name

    return table

def _create_table_object_from_tdmldf(df, table_name, con, primary_index, temporary, schema_name):
    """
    This is an internal function used to construct a SQLAlchemy Table Object.
    Used only for creating Table Objects from TeradataML DataFrames.
    This function checks appropriate flags and supports creation of Teradata
    specific Table constructs such as Volatile/Primary Index tables.

    PARAMETERS:
        df : The TeradataML DataFrame object to be saved.

        table_name : Name of SQL table.

        con : A SQLAlchemy connectable (engine/connection) object

        primary_index : Creates Teradata Table(s) with Primary index column if specified.

        temporary : Flag specifying whether SQL table to be created is Volatile or not.

        schema_name : Specifies the name of the SQL schema in the database to write to.

    RETURNS:
        SQLAlchemy Table

    RAISES:
        N/A

    EXAMPLES:
        _create_table_object_from_tdmldf(df = my_df, table_name = 'test_table', con = tdconnection,
                                         primary_index = None, temporary = True, if_exists = 'replace', schema_name = schema)
    """
    meta = sqlalchemy.MetaData(con)
    meta_cols = df._metaexpr.c

    col_names = [col.name for col in meta_cols]
    col_types = [col.type for col in meta_cols]

    pti = post()

    # Create Table object with appropriate Primary Index/Prefix for volatile
    if primary_index is not None or temporary:
        if primary_index is not None:
            if isinstance(primary_index, list):
                pti = pti.primary_index(unique=True, cols=primary_index)
            else:
                pti = pti.primary_index(unique=True, cols=[primary_index])

        table = Table (table_name, meta,
                   *(Column(col_name, col_type)
                    for col_name, col_type in
                    zip(col_names, col_types)),
                    teradatasql_post_create = pti
                    )

        if temporary:
            table = Table (table_name, meta,
                   *(Column(col_name, col_type)
                    for col_name, col_type in
                    zip(col_names, col_types)),
                    teradatasql_post_create = pti,
                    prefixes=['VOLATILE']
                    )
    # Create Table object without any special PI/Temporary
    else:
        pti = pti.no_primary_index()
        table = Table (table_name, meta,
                   *(Column(col_name, col_type)
                    for col_name, col_type in
                    zip(col_names, col_types)),
                    teradatasql_post_create = pti
                    )

    if schema_name is not None:
        table.schema = schema_name

    return table

def _check_dataframe(df):
    """
    This is an internal function used for DF validation.
    Returns True when object passed is a Pandas or TeradataML DataFrame.
    False otherwise.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

    RETURNS:
        Boolean (True/False)

    RAISES:
        N/A

    EXAMPLES:
        _check_dataframe(df = my_df)

    """
    if isinstance(df, pd.DataFrame) and len(df.columns) > 0:
        return True
    elif isinstance(df, teradataml.dataframe.dataframe.DataFrame) and len(df._metaexpr.c) > 0:
        return True
    else:
        return False

def _check_columns_insertion_compatible(table1_col_object, table2_col_object):
    """
    This is an internal function used to extract column information for two SQLAlchemy ColumnExpression objects;
    and check if column names and types are matching to determine table insertion compatibility.

    PARAMETERS:
        table1_col_object - SQLAlchemy ColumnExpression Object for first table.
        table2_col_object - SQLAlchemy ColumnExpression Object for second table.

    RETURNS:
        a) True, when insertion compatible (names & types match)
        b) False, otherwise

    RAISES:
        N/A

    EXAMPLES:
        _check_columns_insertion_compatible(table1.c, table2.c)

    """
    table1_col_names = [col.name for col in table1_col_object]
    table2_col_names = [col.name for col in table2_col_object]

    if not all(col in table1_col_names for col in table2_col_names):
        return False

    for col_name in table1_col_names:
        if type(table1_col_object[col_name].type) != type(table2_col_object[col_name].type):
            return False

    return True

def _extract_column_info(df):
    """
    This is an internal function used to extract column information for a DF, for Table creation manually.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

    RETURNS:
        a) List of DataFrame Column names
        b) List of equivalent SQLAlchemy Column Types for Pandas Column Types

    RAISES:
        N/A

    EXAMPLES:
        _extract_column_info(df = my_df)

    """
    col_names = df.columns.values.tolist()
    col_types = [_get_sqlalchemy_mapping(str(df.dtypes[key])) for key in list(range(0, len(df.columns)))]
    return col_names, col_types


def _insert_data(df, table_name, con, index, index_label):
    """
    This is an internal function used to pandas.io.sql (to_sql) with 'Append' Mode.
    Used for Default Table creation & to separate Table DDL from Insertions.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

        table_name : Name of SQL table.

        con : A SQLAlchemy connectable (engine/connection) object

        index : Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label : Column label for index column(s).

    RETURNS:
        N/A

    RAISES:
        N/A

    EXAMPLES:
        _insert_data(df = my_df, table_name = 'test_table', con = tdconnection,
                     index = True, index_label = None)
    """
    return df.to_sql(table_name, con, if_exists = 'append', index = False, index_label = index_label)


def _insert_from_dataframe(df, con, table, index, index_name):
    """
    This is an internal function used to to sequentially extract column info from DF,
    iterate rows, and insert rows manually.
    Used for Insertions to Temporary Tables & Tables with Pandas index.

    This uses DBAPI's executeMany() which is a batch insertion method.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

        table_name : Name of SQL table.

        con : A SQLAlchemy connectable (engine/connection) object

        index : Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label : Column label for index column(s).

    RETURNS:
        N/A

    RAISES:
        N/A

    EXAMPLES:
        _insert_from_dataframe(df = my_df, table_name = 'test_table', con = tdconnection,
                               index = True, index_label = None)
    """
    col_names, col_types = _extract_column_info(df)

    insert_list = []
    ins = table.insert()

    for ind, row in df.iterrows():
        ins_dict = {}
        for x in col_names:
            ins_dict[x] = row[x]

        if index is True:
            if index_name in ('', None):
                index_name = 'index_label'
            ins_dict[index_name] = row.name
        insert_list.append(ins_dict)

    #Batch Insertion (using DBAPI's executeMany) used here to insert list of dictionaries
    con.execution_options(autocommit=True).execute(ins, insert_list)

def _insert_sequentially_from_dataframe(df, con, table, index, index_name):
    """
    This is an internal function used to to sequentially extract column info from DF,
    iterate rows, and insert rows manually - Sequentially.
    Used for Insertions to Temporary Tables & Tables with Pandas index
    Encountered to_sql insertion support issues.

    This is a SEQUENTIAL INSERT - In place only until GoSQL Driver supports
    Batch insertion - At which point the above _insert_from_dataframe (which
    Supports BATCH INSERTION) will be used.

    PARAMETERS:
        df : The Pandas DataFrame object to be saved.

        table_name : Name of SQL table.

        con : A SQLAlchemy connectable (engine/connection) object

        index : Flag specifying whether to write Pandas DataFrame index as a column or not.

        index_label : Column label for index column(s).

    RETURNS:
        N/A

    RAISES:
        N/A

    EXAMPLES:
        _insert_from_dataframe(df = my_df, table_name = 'test_table', con = tdconnection,
                               index = True, index_label = None)
    """
    col_names, col_types = _extract_column_info(df)

    columns = []
    values = []

    for ind, row in df.iterrows():
        for x in col_names:
            columns.append(x)
            values.append(row[x])

        if index is True:
            if index_name in ('', None):
                index_name = 'index_label'
            columns.append(index_name)
            values.append(row.name)

        ins_dict = {}
        for col_no in range(len(columns)):
            ins_dict[columns[col_no]] = values[col_no]

        ins = table.insert().values(ins_dict)
        con.execution_options(autocommit=True).execute(ins)

        columns.clear()
        values.clear()

def _get_sqlalchemy_mapping(key):
    """
    This is an internal function used to returns a SQLAlchemy Type Mapping
    for a given Pandas DataFrame column Type.
    Used for Table Object creation internally based on DF column info.

    For an unknown key, String (Mapping to VARCHAR) is returned

    PARAMETERS:
        key : String representing Pandas type ('int64', 'object' etc.)

    RETURNS:
        SQLAlchemy Type (Integer, String, Float, DateTime etc.)

    RAISES:
        N/A

    EXAMPLES:
        _get_sqlalchemy_mapping(key = 'int64')
    """
    teradata_types_map = _get_all_sqlalchemy_mappings()

    if key in teradata_types_map.keys():
        return teradata_types_map.get(key)
    else:
        return String

def _get_all_sqlalchemy_mappings():
    """
    This is an internal function used to return a dictionary of all SQLAlchemy Type Mappings.
    It contains mappings from pandas data type to SQLAlchemyTypes

    PARAMETERS:

    RETURNS:
        dictionary { pandas_type : SQLAlchemy Type}

    RAISES:
        N/A

    EXAMPLES:
        _get_all_sqlalchemy_mappings()
    """
    teradata_types_map = {'int32':Integer, 'int64':BigInteger, 'object':String, 'O':String,
                          'float64':Float, 'float32':Float, 'bool':Boolean,
                          'datetime64':DateTime, 'datetime64[ns]':DateTime,
                          'timedelta64':Interval, 'timedelta[ns]':Interval}

    return teradata_types_map
