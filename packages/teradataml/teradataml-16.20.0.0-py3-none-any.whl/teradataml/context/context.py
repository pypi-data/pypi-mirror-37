# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: rameshchandra.d@teradata.com
Secondary Owner:

teradataml context
----------
A teradataml context functions provide interface to Teradata database. Provides functionality to get and set a global context which
can be used by other analytical functions to get the Teradata database connection.

"""
from sqlalchemy import create_engine
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.sqlbundle import SQLBundle
from teradataml.common.constants import SQLConstants
from teradataml.common.garbagecollector import GarbageCollector
from teradataml.context.aed_context import AEDContext
import warnings
import atexit

#store an global teradata connection.Right now user can only provide an single database connection at any point of time.
td_connection = None
td_sqlalchemy_engine = None
temporary_database_name = None
user_specified_connection = False

def _get_current_databasename():
    """
    Returns the database name associated with the current context.

    PARAMETERS:
        None.

    RETURNS:
        Database name associated with the current context

    RAISES:
        TeradataMlException - If database connection can't be established using the engine.

    EXAMPLES:
        _get_current_databasename()
    """
    if get_connection() is not None:
        try:
            sqlbundle = SQLBundle()
            select_user_query = sqlbundle._get_sql_query(SQLConstants.SQL_SELECT_DATABASE)
            result = get_connection().execute(select_user_query)
            for row in result:
                return row[0]
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, select_user_query),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED) from err
    else:
        return None

def _get_database_username():
    """
    Function to get the database user name.

    PARAMETERS:
        None.

    RETURNS:
        Database user name.

    RAISES:
        TeradataMlException - If "select user" query fails.

    EXAMPLES:
        _get_database_username()
    """
    if get_connection() is not None:
        try:
            sqlbundle = SQLBundle()
            select_query = sqlbundle._get_sql_query(SQLConstants.SQL_SELECT_USER)
            result = get_connection().execute(select_query)
            for row in result:
                return row[0]
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, select_query),
                                      MessageCodes.TDMLDF_EXEC_SQL_FAILED) from err
    else:
        return None

def __cleanup_garbage_collection():
    """initiate the garbage collection."""
    GarbageCollector._cleanup_garbage_collector()

def create_context(host = None, username = None, password = None,  tdsqlengine = None,
                   temp_database_name = None):
    """
    Creates sqlalchemy connection to the Teradata Database using the Teradata ODBC SQL driver by default.
    Users can pass all required parameters (host, username, password) for establishing a connection to Teradata,
    or create a sqlalchemy engine and can pass it to the tdsqlengine parameter.

    PARAMETERS:
        host - The fully qualified domain name or IP address of the Teradata System.
        username - The username for logging onto the Teradata system.
        password - The password required for the username.
        tdsqlengine - Teradata sql-alchemy engine object that should be used to establish a Teradata database connection.
        temp_database_name - The temporary database name where temporary tables, views will be created.

    RETURNS:
        A Teradata sql-alchemy engine object.

    RAISES:
        TeradataMlException - If database connection can't be established.

    EXAMPLES:
        td_sqlalchemy_engine = create_context(host = 'tdhost.labs.teradata.com', username='tduser', password = 'tdpassword')
        td_sqlalchemy_engine = create_context(tdsqlengine = teradata_sql_alchemy_engine)
        td_sqlalchemy_engine = create_context(tdconnection = td_odbc_connection)
    """
    #check if teradata sql alchemy engine is provided by the user
    global td_connection
    global td_sqlalchemy_engine
    global temporary_database_name
    global user_specified_connection
    if tdsqlengine:
        try:
            if td_connection is not None:
                remove_context()
            td_connection = tdsqlengine.connect()
            td_sqlalchemy_engine = tdsqlengine
            user_specified_connection = True
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE) from err
    #check if username & password & host are provided by the user
    elif host and username and password:
        try:
            if td_connection is not None:
                remove_context()
            td_sqlalchemy_engine  = create_engine('teradatasql://'+ username +':' + password + '@'+ host)
            td_connection = td_sqlalchemy_engine.connect()
            user_specified_connection= False
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE) from err

    #assign the tempdatabase name to global
    if temp_database_name is None:
        temporary_database_name = _get_current_databasename()
    else:
        temporary_database_name = temp_database_name

    #connection is established initiate the garbage collection
    atexit.register(__cleanup_garbage_collection)
    __cleanup_garbage_collection()
    # Initialise Dag
    __initalise_dag()
    #return the connection by default
    return td_sqlalchemy_engine

def get_context():
    """
    Return the Teradata database connection associated with the current context.

    PARAMETERS:
        None

    RETURNS:
        A Teradata sql-alchemy engine object.

    RAISES:
        None.

    EXAMPLES:
        td_sqlalchemy_engine = get_context()
    """
    global td_sqlalchemy_engine
    return td_sqlalchemy_engine

def get_connection():
    """
    Return the Teradata database connection associated with the current context.

    PARAMETERS:
        None

    RETURNS:
        A Teradata dbapi connection object.

    RAISES:
        None.

    EXAMPLES:
        tdconnection = get_connection()
    """
    global td_connection
    return td_connection

def set_context(tdsqlengine, temp_database_name = None):
    """
    Set a Teradata database sql alchemy engine as current context.

    PARAMETERS:
        tdsqlengine - A Teradata sql alchemy engine object.
        temp_database_name - The temporary database name where temporary tables, views will be created.

    RETURNS:
        A Teradata database connection.

    RAISES:
        TeradataMlException - If database connection can't be established using the engine.

    EXAMPLES:
        set_context(tdsqlengine = td_sqlalchemy_engine)
    """
    global td_connection
    global td_sqlalchemy_engine
    global temporary_database_name
    if td_connection  is not None:
        warnings.warn(Messages.get_message(MessageCodes.OVERWRITE_CONTEXT))
        remove_context()

    if tdsqlengine:
        try:
            td_connection = tdsqlengine.connect()
            td_sqlalchemy_engine = tdsqlengine
            #assign the tempdatabase name to global
            if temp_database_name is None:
                temporary_database_name = _get_current_databasename()
            else:
                temporary_database_name = temp_database_name
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE) from err
    else:
        return None
    # Initialise Dag
    __initalise_dag()

    return td_connection

def remove_context():
    """
    Removes the current context associated with the Teradata database connection.

    PARAMETERS:
        None.

    RETURNS:
        None.

    RAISES:
        None.

    EXAMPLES:
        remove_context()
    """
    global td_connection
    global td_sqlalchemy_engine
    global user_specified_connection
    if user_specified_connection is not True:
        try:
            #intiate the garbage collection
            __cleanup_garbage_collection()
            td_connection.close()
        except TeradataMlException:
            raise
        except Exception as err:
            raise TeradataMlException(Messages.get_message(MessageCodes.DISCONNECT_FAILURE), MessageCodes.DISCONNECT_FAILURE) from err
    td_connection = None
    td_sqlalchemy_engine = None
    # Closing Dag
    __close_dag()
    return True

def _get_context_temp_databasename():
    """
    Returns the temporary database name associated with the current context.

    PARAMETERS:
        None.

    RETURNS:
        Database name associated with the current context

    RAISES:
        None.

    EXAMPLES:
        _get_context_temp_databasename()
    """
    global temporary_database_name
    return temporary_database_name

def __initalise_dag():
    """
        Intialises the Dag

        PARAMETERS:
            None.

        RETURNS:
            None

        RAISES:
            None.

        EXAMPLES:
            __initalise_dag()
    """
    aed_context = AEDContext()
    # Closing the Dag if previous instance is still exists.
    __close_dag()
    # TODO: Need to add logLevel and log_file functionlaity once AED is implemented these functionalities
    aed_context._init_dag(_get_database_username(),_get_context_temp_databasename(),
                           log_level=4,log_file="")

def __close_dag():
    """
    Closes the Dag

    PARAMETERS:
        None.

    RETURNS:
        None

    RAISES:
        None.

    EXAMPLES:
        __close_dag()
        """
    try:
        AEDContext()._close_dag()
    # Ignore if any exception occurs.
    except TeradataMlException:
        pass
