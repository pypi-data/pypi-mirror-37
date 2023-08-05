# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: rameshchandra.d@teradata.com
Secondary Owner:

teradataml.common.messagecodes
----------
A messages class for holding all message codes related to messages that are displayed to the user
"""

from enum import Enum
import re

class ErrorInfoCodes(Enum):
    """
    This class contains error codes that to be set for the error messages displayed to user.
    The error codes are associated with the respective  messages.
    Information codes are coded with prefix TDML_100x.
    Error codes are prefixed with TDML_200x
    AED error codes with TDML_210x
    Add codes as below whenever required if a new message code added
    """
    # below codes are the information message codes
    CONNECTION_SUCCESS = 'TDML_1000'
    CONNECTION_FAILURE = 'TDML_2000'
    MISSING_ARGS = 'TDML_2001'
    OVERWRITE_CONTEXT = 'TDML_2002'
    FORMULA_INVALID_FORMAT = 'TDML_2003'
    ARG_EMPTY = 'TDML_2004'
    TDF_UNKNOWN_COLUMN = 'TDML_2005'
    DISCONNECT_FAILURE = 'TDML_2006'
    INVALID_ARG_VALUE = 'TDML_2007'
    UNSUPPORTED_DATATYPE = 'TDML_2008'
    SQL_UNKNOWN_KEY = 'TDML_2009'
    TDMLDF_CREATE_FAIL  = 'TDML_2010'
    TDMLDF_EXEC_SQL_FAILED  = 'TDML_2102'
    TDMLDF_CREATE_GARBAGE_COLLECTOR  = 'TDML_2103'
    TDMLDF_DELETE_GARBAGE_COLLECTOR  = 'TDML_2104'
    IS_NOT_VALID_DF  = 'TDML_2011'
    TD_MAX_COL_MESSAGE  = 'TDML_2012'
    INVALID_PRIMARY_INDEX  = 'TDML_2013'
    INDEX_ALREADY_EXISTS  = 'TDML_2015'
    INVALID_INDEX_LABEL = 'TDML_2016'
    TABLE_ALREADY_EXISTS = 'TDML_2019'
    COPY_TO_SQL_FAIL = 'TDML_2020'
    TDMLDF_INFO_ERROR  = 'TDML_2021'
    TDMLDF_UNKNOWN_TYPE = 'TDML_2022'
    TDMLDF_POSITIVE_INT = 'TDML_2024'
    TDMLDF_SELECT_DF_FAIL = 'TDML_2025'
    TDMLDF_SELECT_INVALID_FORMAT = 'TDML_2026'
    TDMLDF_SELECT_INVALID_COLUMN = 'TDML_2027'
    TDMLDF_SELECT_EXPR_UNSPECIFIED = 'TDML_2028'
    TDMLDF_SELECT_NONE_OR_EMPTY = 'TDML_2029'
    INVALID_LENGTH_ARGS = 'TDML_2030'
    TDMLDF_DROP_ARGS = 'TDML_2031'
    TDMLDF_INVALID_DROP_AXIS = 'TDML_2032'
    TDMLDF_DROP_INVALID_COL = 'TDML_2033'
    TDMLDF_DROP_INVALID_INDEX_TYPE = 'TDML_2034'
    TDMLDF_DROP_INVALID_COL_NAMES = 'TDML_2035'
    TDMLDF_DROP_ALL_COLS = 'TDML_2036'
    INVALID_TABLE_NAME_ARGS = 'TDML_2037'
    DROP_TABLE_FAILED = 'TDML_2038'
    EMPTY_DF_RETRIEVED = 'TDML_2039'
    TO_PANDAS_FAILED = 'TDML_2040'
    DF_LABEL_MISMATCH = 'TDML_2041'
    TDMLDF_COLUMN_NOT_FOUND = 'TDML_2042'
    TDMLDF_INVALID_JOIN_CONDITION = "TDML_2043"
    TDMLDF_INVALID_TABLE_ALIAS = "TDML_2044"
    TDMLDF_AGGREGATE_UNSUPPORTED = 'TDML_2045'
    TDMLDF_AGGREGATE_FAILED = 'TDML_2046'
    TDMLDF_INVALID_AGGREGATE_OPERATION = 'TDML_2047'
    INSERTION_INCOMPATIBLE = 'TDML_2048'
    TABLE_OBJECT_CREATION_FAILED = 'TDML_2049'
    FORMULA_MISSING_DEPENDENT_VARIABLE = 'TDML_2050'
    TDMLDF_WRAPPER_ARG_COLUMN_NOT_FOUND = 'TDML_2051'
    INVALID_TABLE_KIND_EMPTY_ARGS = 'TDML_2052'
    LIST_DB_TABLES_FAILED = 'TDML_2053'
    INVALID_CONTEXT_CONNECTION = 'TDML_2054'
    TDMLDF_REQUIRED_TABLE_ALIAS = "TDML_2055"
    TDMLDF_COLUMN_ALREADY_EXISTS = "TDML_2056"
    TDMLDF_AGGREGATE_INVALID_COLUMN = 'TDML_2057'
    TDMLDF_AGGREGATE_COMBINED_ERR = 'TDML_2058'
    DEPENDENT_ARGUMENT = 'TDML_2059'

    # AED Library Error Codes starting from 2100 - Reserved till 2110
    AED_LIBRARY_LOAD_FAIL = 'TDML_2100'
    AED_LIBRARY_NOT_LOADED = 'TDML_2101'
    AED_EXEC_FAILED = 'TDML_2102'
    AED_NON_ZERO_STATUS = 'TDML_2103'
    AED_NODE_COUNT_MISMATCH = 'TDML_2104'
    AED_NODE_QUERY_LENGTH_MISMATCH = 'TDML_2105'
    AED_INVALID_ARGUMENT = 'TDML_2106'
    AED_INVALID_GEN_TABLENAME = 'TDML_2107'
    AED_INVALID_SQLMR_QUERY = 'TDML_2108'
    AED_NODE_ALREADY_EXECUTED = 'TDML_2109'

class MessageCodes(Enum):
    """
    MessageCodes contains all the messages that are displayed to the user which are informational
    or raised when an exception/error occurs.
    Add messages to the class whenever a message need to be displayed to the user
    """
    CONNECTION_SUCCESS              = "Connection successful to Teradata Database."
    CONNECTION_FAILURE              = "Failed to connect to Teradata Database."
    MISSING_ARGS                    = "Following required arguments are missing: {}."
    OVERWRITE_CONTEXT               = "Overwriting an existing context associated with Teradata connection."
    DISCONNECT_FAILURE              = 'Failed to disconnect from Teradata Database.'
    FORMULA_INVALID_FORMAT          = "Invalid formula expression format '{}'"
    ARG_EMPTY                       = "Argument '{}' should not be empty string "
    TDF_UNKNOWN_COLUMN              = "DataFrame does not have column {}"
    INVALID_ARG_VALUE               = "Invalid value(s) '{}' passed to argument '{}', should be: {}."
    SQL_UNKNOWN_KEY                 = "Unable to retrieve SQL text, invalid key."
    TDMLDF_CREATE_FAIL              = "Failed to create Teradata DataFrame."
    AED_LIBRARY_LOAD_FAIL           = "Failed to load AED Library."
    AED_LIBRARY_NOT_LOADED          = "Internal Error: AED Library not loaded. Please make sure AED library is loaded."
    TDMLDF_CREATE_GARBAGE_COLLECTOR = "Error occured while writing to garbage collector file."
    TDMLDF_DELETE_GARBAGE_COLLECTOR = "Error occured while dropping Teradata view/table during garbage cleanup."
    IS_NOT_VALID_DF                 = "DataFrame specified is invalid (None, empty, or unsupported format)."
    TD_MAX_COL_MESSAGE              = "Too many columns in DataFrame, max limit is 2048."
    INVALID_PRIMARY_INDEX           = "Primary index specified not found in DataFrame column list."
    INDEX_ALREADY_EXISTS            = 'Index specified already exists in DataFrame column list.'
    INVALID_INDEX_LABEL             = "Index label specified without index. Provide an index label only when index parameter is True. "
    UNSUPPORTED_DATATYPE            = "Invalid type(s) passed to argument '{}', should be: {}."
    TABLE_ALREADY_EXISTS            = "Table with name {} already exists in database."
    COPY_TO_SQL_FAIL                = "Failed to copy dataframe to Teradata Database."
    TDMLDF_INFO_ERROR               = "Unable to retrieve information for the DataFrame."
    TDMLDF_UNKNOWN_TYPE             = "Invalid type for argument(s) '{}', it should be {}."
    TDMLDF_POSITIVE_INT             = "Value '{}' must be a positive integer greater than 0"
    TDMLDF_EXEC_SQL_FAILED          = "Failed to execute SQL: '{}'"
    TDMLDF_SELECT_DF_FAIL           = "Unable to create new DataFrame while selecting requested columns."
    TDMLDF_SELECT_INVALID_FORMAT    = "Requested column selection format is not supported. " \
                                      "Formats supported are: df.select('col1'), df.select(['col1']), df.select(['col1', 'col2']) " \
                                      "and df.select([['col1', 'col2', 'col3']])."
    TDMLDF_COLUMN_NOT_FOUND         = "Column '{}' not found in {} DataFrame."
    TDMLDF_INVALID_TABLE_ALIAS      = "{} should not be equal."
    TDMLDF_REQUIRED_TABLE_ALIAS     = "Arguments lsuffix or rsuffix should not be None as TeradataML DataFrames contains common column(s)."
    TDMLDF_COLUMN_ALREADY_EXISTS    = "Column name with alias '{}' already exists in {} TeradataML DataFrame, change '{}'"
    TDMLDF_INVALID_JOIN_CONDITION   = "Invalid join condition: '{}', check documentation for valid conditions."
    TDMLDF_SELECT_INVALID_COLUMN    = "Requested column(s) does not exist in parent DataFrame. Valid DataFrame columns for selection are: {}"
    TDMLDF_SELECT_EXPR_UNSPECIFIED  = "Select Expression not specified. Please provide an expression of one of the following formats: " \
                                      "df.select('col1'), df.select(['col1']), df.select(['col1', 'col2']) " \
                                      "or df.select([['col1', 'col2', 'col3']])."
    TDMLDF_SELECT_NONE_OR_EMPTY     = "Select Expression specified contains an empty string/list or an invalid index (such as '', None, [None] or ['None'])."
    INVALID_LENGTH_ARGS             = "Number of values in arguments doesn't match."
    INSERTION_INCOMPATIBLE          = "Unable to perform insertion to existing table; columns do not match. "
    TABLE_OBJECT_CREATION_FAILED    = "Unable to create table definition to save to database."
    TDMLDF_DROP_ARGS                = "Specify at least one of 'labels' OR 'columns'. Single label/columns or list-like label/columns."
    TDMLDF_INVALID_DROP_AXIS        = "Axis can be either (0 or 'index') for index OR (1 or 'columns') for columns"
    TDMLDF_DROP_INVALID_COL         = "Invalid column '{0}', valid columns values are: {1}."
    TDMLDF_DROP_INVALID_INDEX_TYPE  = "Invalid index. Index values must be the same type as the index column type '{}'."
    TDMLDF_DROP_INVALID_COL_NAMES   = "Invalid columns. Column labels must be string values."
    TDMLDF_DROP_ALL_COLS            = "Invalid columns. Cannot drop all columns from DataFrame."
    DF_LABEL_MISMATCH               = "The DataFrame object has a mismatching index with respect to its columns."
    EMPTY_DF_RETRIEVED              = "Dataframe retrieved is empty or of an unsupported format. "
    TO_PANDAS_FAILED                = "Failed to convert dataframe to a Pandas Dataframe. "
    TDMLDF_AGGREGATE_UNSUPPORTED    = "All selected columns [{0}] are unsupported for '{1}' operation."
    TDMLDF_AGGREGATE_FAILED         = "Unable to perform '{0}()' on the dataframe."
    TDMLDF_INVALID_AGGREGATE_OPERATION = "Invalid aggregate operation(s) [{0}] requested on TeradataML DataFrame. Valid aggregate operation(s) are: {1}."
    TDMLDF_AGGREGATE_COMBINED_ERR   = "No results. Below is/are the error message(s):\n{0}"
    TDMLDF_AGGREGATE_INVALID_COLUMN = "Invalid column names(s) [{0}] passed to argument '{1}'. Valid column names are: {2}."
    TDMLDF_AGGREGATE_AGG_DICT_ERR   = "All requested operations on column(s) [{0}] are " \
                                      "unsupported. Please provide at least one valid operation to be performed per column."
    AED_EXEC_FAILED                 = "Internal Error: Failed to execute AED library call."
    AED_NON_ZERO_STATUS             = "Internal Error: Non-zero status returned from AED."
    AED_NODE_COUNT_MISMATCH         = "Internal Error: Node count mismatch for the provided node. Please provide the correct DAG node ID."
    AED_NODE_QUERY_LENGTH_MISMATCH  = "Internal Error: Node query length mismatch for the provided node. Please provide the correct DAG node ID."
    AED_INVALID_ARGUMENT            = "{0} Internal Error: Invalid '{1}', valid types: {2}."
    AED_INVALID_GEN_TABLENAME       = "Internal Error: Temp table name passed to the API, does not have fully qualified name. " \
                                      "Example, Table name must be in 'dbname.tablename' format."
    INVALID_TABLE_NAME_ARGS         = "Argument tablename should not be a empty string or none."
    AED_INVALID_SQLMR_QUERY         = "Internal Error: SQL-MR query must be passed to argument: "
    AED_INVALID_NODE_TYPE           = "Internal Error: Invalid node type (node id) is passed."
    DROP_TABLE_FAILED               = "Drop table failed."
    AED_NODE_ALREADY_EXECUTED       = "Internal Error: Node is already executed. Cannot execute: "
    LIST_DB_TABLES_FAILED           = "Listing of Database Tables failed."
    INVALID_CONTEXT_CONNECTION      = "Current Teradata connection context is empty or not set. Please use create_context or set_context."
    FORMULA_MISSING_DEPENDENT_VARIABLE = "Response/Dependent variable is not specified correctly in the formula."
    TDMLDF_WRAPPER_ARG_COLUMN_NOT_FOUND = "Column '{}' provided in '{}' argument, does not exist in '{}' DataFrame."
    DEPENDENT_ARGUMENT = "'{}' can only be used when '{}' is specified (not None)."
