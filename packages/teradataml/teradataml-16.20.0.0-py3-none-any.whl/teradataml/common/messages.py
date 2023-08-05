# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: rameshchandra.d@teradata.com
Secondary Owner:

teradataml.common.messages
----------
A messages class for holding all text messages that are displayed to the user
"""
from teradataml.common import messagecodes
from teradataml.common.messagecodes import ErrorInfoCodes
from teradataml.common.messagecodes import MessageCodes

class Messages():
    """
    Contains list of messages with respective error codes
    Add new error and message codes in self.messages list whenever codes are added in errormessagecodes
    file.
    """
    __messages = []
    __standard_message = "[Teradata][teradataml]"
    __messages = [
            [ErrorInfoCodes.CONNECTION_SUCCESS, MessageCodes.CONNECTION_SUCCESS],
            [ErrorInfoCodes.CONNECTION_FAILURE, MessageCodes.CONNECTION_FAILURE],
            [ErrorInfoCodes.DISCONNECT_FAILURE, MessageCodes.DISCONNECT_FAILURE],
            [ErrorInfoCodes.MISSING_ARGS, MessageCodes.MISSING_ARGS],
            [ErrorInfoCodes.OVERWRITE_CONTEXT, MessageCodes.OVERWRITE_CONTEXT],
            [ErrorInfoCodes.FORMULA_INVALID_FORMAT, MessageCodes.FORMULA_INVALID_FORMAT],
            [ErrorInfoCodes.ARG_EMPTY, MessageCodes.ARG_EMPTY],
            [ErrorInfoCodes.INVALID_ARG_VALUE, MessageCodes.INVALID_ARG_VALUE],
            [ErrorInfoCodes.TDF_UNKNOWN_COLUMN, MessageCodes.TDF_UNKNOWN_COLUMN],
            [ErrorInfoCodes.AED_LIBRARY_LOAD_FAIL, MessageCodes.AED_LIBRARY_LOAD_FAIL],
            [ErrorInfoCodes.AED_LIBRARY_NOT_LOADED, MessageCodes.AED_LIBRARY_NOT_LOADED],
            [ErrorInfoCodes.AED_EXEC_FAILED, MessageCodes.AED_EXEC_FAILED],
            [ErrorInfoCodes.AED_NON_ZERO_STATUS, MessageCodes.AED_NON_ZERO_STATUS],
            [ErrorInfoCodes.AED_NODE_COUNT_MISMATCH, MessageCodes.AED_NODE_COUNT_MISMATCH],
            [ErrorInfoCodes.AED_NODE_QUERY_LENGTH_MISMATCH, MessageCodes.AED_NODE_QUERY_LENGTH_MISMATCH],
            [ErrorInfoCodes.AED_INVALID_ARGUMENT, MessageCodes.AED_INVALID_ARGUMENT],
            [ErrorInfoCodes.AED_INVALID_GEN_TABLENAME, MessageCodes.AED_INVALID_GEN_TABLENAME],
            [ErrorInfoCodes.AED_INVALID_SQLMR_QUERY, MessageCodes.AED_INVALID_SQLMR_QUERY],
            [ErrorInfoCodes.AED_NODE_ALREADY_EXECUTED, MessageCodes.AED_NODE_ALREADY_EXECUTED],
            [ErrorInfoCodes.SQL_UNKNOWN_KEY, MessageCodes.SQL_UNKNOWN_KEY],
            [ErrorInfoCodes.TDMLDF_CREATE_FAIL, MessageCodes.TDMLDF_CREATE_FAIL],
            [ErrorInfoCodes.TDMLDF_EXEC_SQL_FAILED, MessageCodes.TDMLDF_EXEC_SQL_FAILED],
            [ErrorInfoCodes.TDMLDF_CREATE_GARBAGE_COLLECTOR, MessageCodes.TDMLDF_CREATE_GARBAGE_COLLECTOR],
            [ErrorInfoCodes.TDMLDF_DELETE_GARBAGE_COLLECTOR, MessageCodes.TDMLDF_DELETE_GARBAGE_COLLECTOR],
            [ErrorInfoCodes.IS_NOT_VALID_DF, MessageCodes.IS_NOT_VALID_DF],
            [ErrorInfoCodes.TD_MAX_COL_MESSAGE, MessageCodes.TD_MAX_COL_MESSAGE],
            [ErrorInfoCodes.INVALID_PRIMARY_INDEX, MessageCodes.INVALID_PRIMARY_INDEX],
            [ErrorInfoCodes.INDEX_ALREADY_EXISTS, MessageCodes.INDEX_ALREADY_EXISTS],
            [ErrorInfoCodes.INVALID_INDEX_LABEL, MessageCodes.INVALID_INDEX_LABEL],
            [ErrorInfoCodes.TABLE_ALREADY_EXISTS, MessageCodes.TABLE_ALREADY_EXISTS],
            [ErrorInfoCodes.COPY_TO_SQL_FAIL, MessageCodes.COPY_TO_SQL_FAIL],
            [ErrorInfoCodes.TDMLDF_INFO_ERROR, MessageCodes.TDMLDF_INFO_ERROR],
            [ErrorInfoCodes.TDMLDF_UNKNOWN_TYPE, MessageCodes.TDMLDF_UNKNOWN_TYPE],
            [ErrorInfoCodes.TDMLDF_POSITIVE_INT, MessageCodes.TDMLDF_POSITIVE_INT],
            [ErrorInfoCodes.TDMLDF_SELECT_DF_FAIL, MessageCodes.TDMLDF_SELECT_DF_FAIL],
            [ErrorInfoCodes.TDMLDF_SELECT_INVALID_FORMAT, MessageCodes.TDMLDF_SELECT_INVALID_FORMAT],
            [ErrorInfoCodes.TDMLDF_SELECT_INVALID_COLUMN, MessageCodes.TDMLDF_SELECT_INVALID_COLUMN],
            [ErrorInfoCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED, MessageCodes.TDMLDF_SELECT_EXPR_UNSPECIFIED],
            [ErrorInfoCodes.TDMLDF_SELECT_NONE_OR_EMPTY, MessageCodes.TDMLDF_SELECT_NONE_OR_EMPTY],
            [ErrorInfoCodes.INVALID_LENGTH_ARGS, MessageCodes.INVALID_LENGTH_ARGS],
            [ErrorInfoCodes.INVALID_TABLE_NAME_ARGS, MessageCodes.INVALID_TABLE_NAME_ARGS],
            [ErrorInfoCodes.UNSUPPORTED_DATATYPE, MessageCodes.UNSUPPORTED_DATATYPE],
            [ErrorInfoCodes.TDMLDF_DROP_ARGS, MessageCodes.TDMLDF_DROP_ARGS],
            [ErrorInfoCodes.TDMLDF_INVALID_DROP_AXIS, MessageCodes.TDMLDF_INVALID_DROP_AXIS],
            [ErrorInfoCodes.TDMLDF_DROP_INVALID_COL, MessageCodes.TDMLDF_DROP_INVALID_COL],
            [ErrorInfoCodes.TDMLDF_DROP_INVALID_INDEX_TYPE, MessageCodes.TDMLDF_DROP_INVALID_INDEX_TYPE],
            [ErrorInfoCodes.TDMLDF_DROP_INVALID_COL_NAMES, MessageCodes.TDMLDF_DROP_INVALID_COL_NAMES],
            [ErrorInfoCodes.TDMLDF_DROP_ALL_COLS, MessageCodes.TDMLDF_DROP_ALL_COLS],
            [ErrorInfoCodes.LIST_DB_TABLES_FAILED, MessageCodes.LIST_DB_TABLES_FAILED],
            [ErrorInfoCodes.INVALID_CONTEXT_CONNECTION, MessageCodes.INVALID_CONTEXT_CONNECTION],
            [ErrorInfoCodes.DF_LABEL_MISMATCH, MessageCodes.DF_LABEL_MISMATCH],
            [ErrorInfoCodes.EMPTY_DF_RETRIEVED, MessageCodes.EMPTY_DF_RETRIEVED],
            [ErrorInfoCodes.TO_PANDAS_FAILED, MessageCodes.TO_PANDAS_FAILED],
            [ErrorInfoCodes.TDMLDF_INVALID_JOIN_CONDITION, MessageCodes.TDMLDF_INVALID_JOIN_CONDITION],
            [ErrorInfoCodes.TDMLDF_INVALID_TABLE_ALIAS, MessageCodes.TDMLDF_INVALID_TABLE_ALIAS],
            [ErrorInfoCodes.TDMLDF_REQUIRED_TABLE_ALIAS, MessageCodes.TDMLDF_REQUIRED_TABLE_ALIAS],
            [ErrorInfoCodes.TDMLDF_COLUMN_ALREADY_EXISTS, MessageCodes.TDMLDF_COLUMN_ALREADY_EXISTS],
            [ErrorInfoCodes.INVALID_LENGTH_ARGS, MessageCodes.INVALID_LENGTH_ARGS],
            [ErrorInfoCodes.TDMLDF_COLUMN_NOT_FOUND, MessageCodes.TDMLDF_COLUMN_NOT_FOUND],
            [ErrorInfoCodes.TDMLDF_AGGREGATE_UNSUPPORTED, MessageCodes.TDMLDF_AGGREGATE_UNSUPPORTED],
            [ErrorInfoCodes.TDMLDF_AGGREGATE_FAILED, MessageCodes.TDMLDF_AGGREGATE_FAILED],
            [ErrorInfoCodes.TDMLDF_INVALID_AGGREGATE_OPERATION, MessageCodes.TDMLDF_INVALID_AGGREGATE_OPERATION],
            [ErrorInfoCodes.INSERTION_INCOMPATIBLE, MessageCodes.INSERTION_INCOMPATIBLE],
            [ErrorInfoCodes.TABLE_OBJECT_CREATION_FAILED, MessageCodes.TABLE_OBJECT_CREATION_FAILED],
            [ErrorInfoCodes.FORMULA_MISSING_DEPENDENT_VARIABLE, MessageCodes.FORMULA_MISSING_DEPENDENT_VARIABLE],
            [ErrorInfoCodes.TDMLDF_WRAPPER_ARG_COLUMN_NOT_FOUND, MessageCodes.TDMLDF_WRAPPER_ARG_COLUMN_NOT_FOUND],
            [ErrorInfoCodes.TDMLDF_AGGREGATE_INVALID_COLUMN, MessageCodes.TDMLDF_AGGREGATE_INVALID_COLUMN],
            [ErrorInfoCodes.TDMLDF_AGGREGATE_COMBINED_ERR, MessageCodes.TDMLDF_AGGREGATE_COMBINED_ERR],
            [ErrorInfoCodes.DEPENDENT_ARGUMENT, MessageCodes.DEPENDENT_ARGUMENT],
            [ErrorInfoCodes.DROP_TABLE_FAILED, MessageCodes.DROP_TABLE_FAILED]
            
    ]

    @staticmethod
    def get_message(messagecode, *variables, **kwargs):
        """
        Generate a message associated with stanadard message and error code .

        PARAMETERS:
            messagecode(Required)  - Message  to be returned to the user when needed to be raised based on \
                                    the associated  MessageCode
            variables(Optional) -   List of arguments to mention if any missing arguments.
            kwargs(Optional)  - dictionary of keyword arguments for displaying the key and its desired value .

        RETURNS:
            Message with standard python message and message code.


        RAISES:

        EXAMPLES:
            from teradataml.common.messagecodes import MessageCodes
            from teradataml.common.messages import Messages
            Messages.get_message(MessageCodes.TDMLDF_UNKNOWN_REFERENCE_TYPE, "arg_name","data")
            msg = messages._getMessage(messagecode = MessageCodes.TABLE_CREATE)
            msg = messages._getMessage(messagecode = MessageCodes.MISSING_ARGS,missArgs)

        """
        for msg in Messages.__messages:
            if msg[1] == messagecode :
                message = "{}({}) {}".format(Messages.__standard_message, msg[0].value, msg[1].value)
                if len(variables) != 0:
                    message = message.format(*variables)
                if len(kwargs) != 0 :
                    message = "{} {}".format(message, kwargs)

        return message
