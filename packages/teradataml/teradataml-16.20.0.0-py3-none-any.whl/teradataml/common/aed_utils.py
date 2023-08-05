"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pankajvinod.purandare@teradata.com
Secondary Owner:

This file implements the wrapper's around AED API's from eleCommon library.
This facilitates the teradataml library infrastructure code to call these functions
and not change anything in future, regardless, of the design changes on
AED side.
"""

import os
import platform
import re

from ctypes import c_int, c_char_p, c_char, POINTER, byref

from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.messages import Messages
from teradataml.common.utils import UtilFuncs
from teradataml.common.constants import AEDConstants
from teradataml.common.constants import SQLPattern
from teradataml.context.aed_context import AEDContext


class AedUtils:

    def __init__(self):
        self.aed_context = AEDContext()

    def _aed_table(self, source):
        """
        This wrapper function facilitates a integration with 'aed_table',
        a C++ function, in AED library, with Python tdml library.

        This  function must be called when a Python (tdml) data frame is to be
        created using a table name.

        PARAMETERS:
            source - Fully qualified source table name i.e. dbname.tablename

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")

        RETURNS:
            A node id in DAG - AED, for a data frame.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_table.argtypes =[POINTER(c_char_p),
                                                             POINTER(c_char_p),
                                                             POINTER(c_char_p),
                                                             POINTER(c_char_p),
                                                             POINTER(c_char_p),
                                                             POINTER(c_int)
                                                 ]
        # Input arguments for 'C' function.
        arg_name = ["source"]
        arg_value = [source]
        output_table = [""]
        output_schema = [""]

        # Ouptut nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])

        # return code
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request for TABLE
            self.aed_context.ele_common_lib.aed_table(self.aed_context._arr_c(arg_name),
                                          self.aed_context._arr_c(arg_value),
                                          self.aed_context._arr_c(output_table),
                                          self.aed_context._arr_c(output_schema),
                                          nodeid_out,
                                          ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_table)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))

    def _aed_query(self, query, temp_table_name=None):
        """
        This wrapper function facilitates a integration with 'aed_query',
        a C++ function, in AED library, with Python tdml library.

        This  function must be called when a Python (tdml) data frame is to be
        created using a SQL query.

        PARAMETERS:
            query - SQL query
            temp_table_name - Temporary table name to be used for output of aed_query node.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_query("select * from table")

        RETURNS:
            A node id in DAG - AED, for a data frame.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_query.argtypes =[POINTER(c_char_p),
                                                 POINTER(c_char_p),
                                                 POINTER(c_char_p),
                                                 POINTER(c_char_p),
                                                 POINTER(c_char_p),
                                                 POINTER(c_int)
                                                 ]

        # Input arguments for 'C' function.
        arg_name = ["source"]
        arg_value = [query]
        if temp_table_name is None:
            temp_table_name = UtilFuncs._generate_temp_table_name(prefix="query_", use_default_database=True, quote=False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]
        if output_schema[0] is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_INVALID_GEN_TABLENAME,
                                                           "(aed_query) :: Received tablename as - {}".format(temp_table_name)),
                                      MessageCodes.AED_INVALID_GEN_TABLENAME)

        # Ouptut nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])

        # return code
        ret_code = self.aed_context._int_array1(0)

        try:
            self.aed_context.ele_common_lib.aed_query(self.aed_context._arr_c(arg_name),
                                          self.aed_context._arr_c(arg_value),
                                          self.aed_context._arr_c(output_table),
                                          self.aed_context._arr_c(output_schema),
                                          nodeid_out,
                                          ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_query)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))

    def _aed_select(self, nodeid, select_expr):
        """
        This wrapper function facilitates a integration with 'aed_select',
        a C++ function, in AED library, with Python tdml library.

        This function must be called when a SELECT operation that is
        columns are to be selected from a Python (tdml) data frame.

        PARAMETERS:
            nodeid - A DAG node, a input to the select API.
            select_expr - Columns, to be selected from the data frame.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")

        RETURNS:
            A node id in DAG - AED select API.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_select.argtypes =[POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_int)
                                                  ]

        arg_name = ["projection"]
        arg_value = [select_expr]
        temp_table_name = UtilFuncs._generate_temp_table_name(prefix="select_", use_default_database=True, quote=False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]

        # Output nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])

        # return code
        ret_code = self.aed_context._int_array1(0)
        try:
            # *** AED request to select columns
            self.aed_context.ele_common_lib.aed_select(self.aed_context._arr_c([nodeid]),
                                           self.aed_context._arr_c(arg_name),
                                           self.aed_context._arr_c(arg_value),
                                           self.aed_context._arr_c(output_table),
                                           self.aed_context._arr_c(output_schema),
                                           nodeid_out,
                                           ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_select)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))

    def _aed_aggregate(self, nodeid, aggregate_expr, operation):
        """
        This wrapper function facilitates a integration with
        'aed_aggregate', a C++ function, in AED library, with Python
        tdml library.

        This function must be called when an aggregate functions like
        MIN, MAX, AVG are to be performed on dataframe columns

        PARAMETERS:
            nodeid - String. It is a DAG node which is given as an
                     input to the aggregate API.
            aggregate_expr - String. Expressions like
                        'min(col1) as min_col1, min(col2) as min_col2'
                     or 'max(col1) as max_col1, max(col2) as max_col2'
            operation - String. Aggregate Operation to be performed on
                        the columns eg. min

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_aggregate_nodeid = AedObj._aed_aggregate(
                            aed_table_nodeid, "min(col1) as min_col1,
                            min(col2) as min_col2", operation = 'min')
            aed_aggregate_nodeid1 = AedObj._aed_aggregate(
                            aed_table_nodeid, "max(col1) as max_col1,
                            max(col2) as max_col2", operation = 'max')

        RETURNS:
            A node id in DAG - AED aggregate API.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """

        # Specify the argument types
        self.aed_context.ele_common_lib.aed_aggregate.argtypes = [POINTER(c_char_p),
                                                               POINTER(c_char_p),
                                                               POINTER(c_char_p),
                                                               POINTER(c_char_p),
                                                               POINTER(c_char_p),
                                                               POINTER(c_char_p),
                                                               POINTER(c_int)
                                                               ]
        arg_name = ["expr"]
        arg_value = [aggregate_expr]
        temp_table_name = UtilFuncs._generate_temp_table_name(
                                    prefix = "aggregate_" + operation + "_",
                                    use_default_database = True, quote = False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]

        # Output nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])

        # return code
        ret_code = self.aed_context._int_array1(0)
        try:
            # *** AED request to get aggregate of columns
            self.aed_context.ele_common_lib.aed_aggregate(self.aed_context._arr_c([nodeid]),
                                                       self.aed_context._arr_c(arg_name),
                                                       self.aed_context._arr_c(arg_value),
                                                       self.aed_context._arr_c(output_table),
                                                       self.aed_context._arr_c(output_schema),
                                                       nodeid_out,
                                                       ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message( MessageCodes.AED_EXEC_FAILED,
                "(aed_aggregate_" + operation + ")" + str(emsg)), MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0],
                                                            nodeid_out[0].decode("utf-8"))

    def _aed_filter(self, nodeid, filter_expr):
        """
        This wrapper function facilitates a integration with 'aed_filter',
        a C++ function, in AED library, with Python tdml library.

        This function must be called when a FILTER operation that is
        results needs to filtered from a Python (tdml) data frame.

        PARAMETERS:
            nodeid - A DAG node, a input to the filter API.
            filter_expr - Expression in SQL format, to be used to filter data from the data frame.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            aed_filter_nodeid = AedObj._aed_filter(aed_select_nodeid, "col1 > col2")

        RETURNS:
            A node id in DAG - AED filter API.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_filter.argtypes =[POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_int)
                                                  ]

        arg_name = ["projection"]
        arg_value = [filter_expr]
        temp_table_name = UtilFuncs._generate_temp_table_name(prefix="filter_", use_default_database=True, quote=False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]

        # Output nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])

        # return code
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request to filter
            self.aed_context.ele_common_lib.aed_filter(self.aed_context._arr_c([nodeid]),
                                           self.aed_context._arr_c(arg_name),
                                           self.aed_context._arr_c(arg_value),
                                           self.aed_context._arr_c(output_table),
                                           self.aed_context._arr_c(output_schema),
                                           nodeid_out,
                                           ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_filter)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))

    def _aed_ml_query(self, inp_nodeids, query, output_tables, function_name):
        """
        This wrapper function facilitates a integration with 'aed_ml_query',
        a C++ function, in AED library, with Python tdml library.

        This  function must be called when a Python (tdml) wrapper functions to generate
        DAG node for analytical queries.

        PARAMETERS:
            inp_nodeids - A list of input table/query nodeids.
            query - Complete SQL-MR query
            output_tables - List of output table names to be used for output of aed_ml_query node.
            function_name - Analytical function name.

        EXAMPLES:
            nodeid_out = self.aedObj._aed_ml_query([inp_node_id1, inp_node_id2], sqlmr_query, [stdout_table, out_table1, out_table2],
                                               "Sessionize")

        RETURNS:
            Returns a list of node ids corresponding to each output table, starting with STDOUT table and then
            SQL-MR output tables.

        RAISES:
            Teradataml exceptions:
                AED_INVALID_SQLMR_QUERY, AED_INVALID_GEN_TABLENAME, AED_EXEC_FAILED and AED_NON_ZERO_STATUS
            TypeErrors - For internal errors. For type mismatch.

        """

        if not isinstance(inp_nodeids, list) or not all(isinstance(nodeid, str) for nodeid in inp_nodeids):
            raise TypeError("AED Internal Error: 'inp_nodeids' should be of type list containing strings.")

        if not isinstance(query, str):
            raise TypeError("AED Internal Error: 'query' should be of type str.")

        if not isinstance(output_tables, list) or not all(isinstance(otab, str) for otab in output_tables):
            raise TypeError("AED Internal Error: 'output_tables' should be of type list containing strings.")

        if not isinstance(function_name, str):
            raise TypeError("AED Internal Error: 'function_name' should be of type str")

        if not SQLPattern.SQLMR.match(query):
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_INVALID_SQLMR_QUERY, "query (aed_ml_query)"),
                                          MessageCodes.AED_INVALID_SQLMR_QUERY)

        # Specify the argument types
        self.aed_context.ele_common_lib.aed_ml_query.argtypes =[POINTER(c_char_p),  # Node Ids
                                                                 POINTER(c_char_p),  # arg_name
                                                                 POINTER(c_char_p),  # arg_value
                                                                 POINTER(c_char_p),  # output_table
                                                                 POINTER(c_char_p),  # output_schema
                                                                 POINTER(c_char_p),  # function_name
                                                                 POINTER(c_int),     # Num of Inputs
                                                                 POINTER(c_int),     # Num of Outputs
                                                                 POINTER(c_char_p),  # Output Node Ids
                                                                 POINTER(c_int)      # Return code
                                                                 ]

        # Input arguments for 'C' function.
        arg_name = ["source"]
        arg_value = [query]

        # Input and Output Lengths
        num_inputs = len(inp_nodeids)
        num_outputs = len(output_tables)

        # Ouptut nodeids
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"] * num_outputs)
        output_table_names = []
        output_schemas = []
        for index in range(num_outputs):
            output_table_names.append(UtilFuncs._extract_table_name(output_tables[index]))
            output_schemas.append(UtilFuncs._extract_db_name(output_tables[index]))
            if output_schemas[index] is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.AED_INVALID_GEN_TABLENAME, "(aed_ml_query) " + output_tables[index]),
                                          MessageCodes.AED_INVALID_GEN_TABLENAME)

        # return code
        ret_code = self.aed_context._int_array1(0)

        try:
            self.aed_context.ele_common_lib.aed_ml_query(self.aed_context._arr_c(inp_nodeids),
                                             self.aed_context._arr_c(arg_name),
                                             self.aed_context._arr_c(arg_value),
                                             self.aed_context._arr_c(output_table_names),
                                             self.aed_context._arr_c(output_schemas),
                                             self.aed_context._arr_c([function_name]),
                                             self.aed_context._int_array1(num_inputs),
                                             self.aed_context._int_array1(num_outputs),
                                             nodeid_out,
                                             ret_code)
            output_nodeids = self.aed_context._decode_list(nodeid_out)
            del nodeid_out
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_ml_query)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], output_nodeids)

    def _aed_gen_dag_path(self, nodeid):
        """
        This wrapper function facilitates a integration with 'aed_filter',
        a C++ function, in AED library, with Python tdml library.

        This function must be called with DAG node id, when a complete DAG
        path for the node is to be generated.
        Most of the times, user must call _aed_get_exec_query, which will call
        this particular function too.

        PARAMETERS:
            nodeid - A DAG node id for which DAG path needs to be genertaed.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            aed_filter_nodeid = AedObj._aed_filter(aed_select_nodeid, "col1 > col2")
            num_nodes = AedObj._aed_gen_dag_path(aed_filter_nodeid)

        RETURNS:
            Number of DAG nodes involved in the DAG path for the provided node ID.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_gen_dag_path.argtypes = [POINTER(c_char_p),
                                                         POINTER(c_int),
                                                         POINTER(c_int)
                                                         ]

        dag_node_count = self.aed_context._int_array1(0)
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request to generate DAG path
            self.aed_context.ele_common_lib.aed_gen_dag_path(self.aed_context._arr_c([nodeid]), dag_node_count, ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_gen_dag_path)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], dag_node_count[0])

    def _aed_get_dag_querysize(self, nodeid, dag_path_node_count=None):
        """
        This wrapper function facilitates a integration with 'aed_get_dag_querysize',
        a C++ function, in AED library, with Python tdml library.

        This function is called to get the length of the queries involved in the
        DAG path nodes.

        PARAMETERS:
            nodeid - A DAG node ID for which query size needs to be calculated.
            dag_path_node_count - Number of DAG nodes involved in the DAG path.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            num_nodes = AedObj._aed_gen_dag_path(aed_select_nodeid)
            qry_size = AedObj._aed_get_dag_querysize(aed_select_nodeid, num_nodes)

        RETURNS:
            dag_query_size - Query size for the DAG path for all nodes.

        RAISES:
             Teradataml exceptions:
                AED_NODE_COUNT_MISMATCH, AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_get_dag_querysize.argtypes = [POINTER(c_char_p),
                                                              POINTER(c_int),
                                                              POINTER(c_int),
                                                              POINTER(c_int)
                                                              ]

        # Let's validate the provided dag path node count.
        dag_path_node_count_verify = self._aed_gen_dag_path(nodeid)
        if dag_path_node_count is None:
            # Check if DAG node count for the provided node_id is given or not.
            dag_path_node_count = dag_path_node_count_verify

        elif dag_path_node_count != dag_path_node_count_verify:
            # If provided and does not match with the actual one, raise exception.
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_NODE_COUNT_MISMATCH, "(aed_get_dag_querysize)"),
                MessageCodes.AED_NODE_COUNT_MISMATCH)

        if self._aed_is_node_executed(nodeid):
            # If node is already executed, then we do not need to run _aed_get_dag_querysize
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_NODE_ALREADY_EXECUTED, "(aed_get_dag_querysize)"),
                MessageCodes.AED_NODE_ALREADY_EXECUTED)

        int_array_n = c_int * dag_path_node_count
        dag_query_size = int_array_n(0)
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request to get DAG query size
            self.aed_context.ele_common_lib.aed_get_dag_querysize(self.aed_context._arr_c([nodeid]),
                                                                  c_int(dag_path_node_count), dag_query_size, ret_code)
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_get_dag_querysize)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

        dag_query_size = [qry_size for qry_size in dag_query_size]
        return self.aed_context._validate_aed_return_code(ret_code[0], dag_query_size)

    def _aed_get_exec_query(self, nodeid, dag_path_node_count=None, dag_query_len=None):
        """
        This wrapper function facilitates a integration with 'aed_get_exec_query',
        a C++ function, in AED library, with Python tdml library.

        This function must be called when all the queries in the required node to
        be constructed and executed on Python client.

        PARAMETERS:
            nodeid - A DAG node ID for which queries involved in DAG path are to be retrieved.
            dag_path_node_count - Number of DAG nodes involved in the DAG path.
            dag_query_len - Query size for the DAG path for all nodes.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            num_nodes = AedObj._aed_get_exec_query(aed_select_nodeid)

        RETURNS:
            A list of list, where first list has strings (table/view) to be created upon execution of SQL.
            And second list has equivalent SQL queries, those needs to be executed for complete execution
            of a node.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_get_exec_query.argtypes = [POINTER(c_char_p),
                                                           POINTER(c_int),
                                                           POINTER(c_char_p),
                                                           POINTER(c_char_p),
                                                           POINTER(c_char_p),
                                                           POINTER(c_char_p),
                                                           POINTER(c_int)
                                                           ]

        if self._aed_is_node_executed(nodeid):
            # If node is already executed, then we do not need to run _aed_get_dag_querysize
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_NODE_ALREADY_EXECUTED, "(_aed_get_exec_query)"),
                MessageCodes.AED_NODE_ALREADY_EXECUTED)

        # Validate the provided dag path node count.
        dag_path_node_count_verify = self._aed_gen_dag_path(nodeid)
        if dag_path_node_count is None:
            # Check if DAG node count for the provided node_id is given or not.
            dag_path_node_count = dag_path_node_count_verify

        elif dag_path_node_count != dag_path_node_count_verify:
            # If provided and does not match with the actual one, raise exception.
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_NODE_COUNT_MISMATCH, "(_aed_get_exec_query)"),
                MessageCodes.AED_NODE_COUNT_MISMATCH)

        # Validate the provided dag query length.
        if dag_query_len is not None:
            if not isinstance(dag_query_len, list) or not all(isinstance(size, int) for size in dag_query_len):
                raise TypeError("AED Internal Error: 'dag_query_len' should be of type list containing integers.")

        dag_query_len_verify = self._aed_get_dag_querysize(nodeid, dag_path_node_count)
        if dag_query_len is None:
            dag_query_len = dag_query_len_verify

        elif dag_query_len != dag_query_len_verify:
            # If provided and does not match with the actual one, raise exception.
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_NODE_QUERY_LENGTH_MISMATCH, "(_aed_get_exec_query)"
                                     + str(dag_query_len) + " and " + str(dag_query_len_verify)),
                MessageCodes.AED_NODE_QUERY_LENGTH_MISMATCH)

        # dag_query_len contains a list of integers, for all the queries included in DAG PATH.
        # Accordingly, let's construct a query buffer.
        query_buffer = []
        for index in range(len(dag_query_len)):
            query_buffer.append(" " * dag_query_len[index])
        query_buffer = self.aed_context._arr_c(query_buffer)

        # Let's construct a table name buffer.
        table_name_buffer = self.aed_context._arr_c(
            [" " * AEDConstants.AED_DB_OBJECT_NAME_BUFFER_SIZE.value * 2] * dag_path_node_count)
        node_type_buffer = self.aed_context._arr_c(
            [" " * AEDConstants.AED_NODE_TYPE_BUFFER_SIZE.value] * dag_path_node_count)
        node_id_buffer = self.aed_context._arr_c(["00000000000000000000"] * dag_path_node_count)
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request to generate queries
            self.aed_context.ele_common_lib.aed_get_exec_query(self.aed_context._arr_c([nodeid]),
                                                   c_int(dag_path_node_count),
                                                   query_buffer,
                                                   table_name_buffer,
                                                   node_type_buffer,
                                                   node_id_buffer,
                                                   ret_code)
            # Decode UTF-8 strings
            table_name_buffer_out = self.aed_context._decode_list(table_name_buffer)
            del table_name_buffer
            query_buffer_out = self.aed_context._decode_list(query_buffer)
            del query_buffer
            node_type_out = self.aed_context._decode_list(node_type_buffer)
            del node_type_buffer
            node_id_out = self.aed_context._decode_list(node_id_buffer)
            del node_id_buffer

        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_get_exec_query)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], [table_name_buffer_out, query_buffer_out,
                                                                        node_type_out, node_id_out])

    def _aed_update_node_state(self, nodeid, nodestate=AEDConstants.AED_NODE_EXECUTED.value):
        """
        This wrapper function facilitates a integration with 'aed_update_node_state',
        a C++ function, in AED library, with Python tdml library.

        A function to update all the nodes in the DAG node path, when executed
        from client. This function needs to be called once all the node queries
        have been executed.

        PARAMETERS:
            nodeid - A DAG node ID for which node state has to updated.
            nodestate - Node state to which node should be updated.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            tables_queries = AedObj._aed_get_exec_query(aed_select_nodeid)
            num_nodes_updated = AedObj._aed_update_node_state(self, nodeid)

        RETURNS:
            Returns number of DAG Nodes updated.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_update_node_state.argtypes = [POINTER(c_char_p),
                                                           POINTER(c_int),
                                                           POINTER(c_int),
                                                           POINTER(c_int)
                                                           ]

        ret_code = self.aed_context._int_array1(0)
        # TODO - need to assign zero once AED issue is fixed
        num_dag_nodes = self.aed_context._int_array1(1)

        if nodestate not in (AEDConstants.AED_NODE_NOT_EXECUTED.value, AEDConstants.AED_NODE_EXECUTED.value):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_INVALID_ARGUMENT, "(_aed_update_node_state)", "nodestate",
                                     [AEDConstants.AED_NODE_NOT_EXECUTED.value, AEDConstants.AED_NODE_EXECUTED.value]),
                MessageCodes.AED_INVALID_ARGUMENT)

        try:
            # # *** AED request to update node states of a DAG
            self.aed_context.ele_common_lib.aed_update_node_state(self.aed_context._arr_c([nodeid]),
                                                                  c_int(nodestate), num_dag_nodes, ret_code)
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_update_node_state)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], num_dag_nodes[0])

    def _aed_update_node_state_single(self, nodeid, nodestate=AEDConstants.AED_NODE_EXECUTED.value):
        """
        This wrapper function facilitates a integration with 'aed_update_node_state_single',
        a C++ function, in AED library, with Python tdml library.

        A function to update a node id of DAG to executed state.
        This function needs to be called when to update single node state to execute.

        PARAMETERS:
            nodeid - A DAG node ID for which node state has to updated.
            nodestate - Node state to which node should be updated.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            AedObj._aed_update_node_state_single(self, aed_select_nodeid)

        RETURNS:
            None

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_update_node_state_single.argtypes = [POINTER(c_char_p),
                                                                          POINTER(c_int),
                                                                          POINTER(c_int)
                                                                          ]

        ret_code = self.aed_context._int_array1(0)

        if nodestate not in (AEDConstants.AED_NODE_NOT_EXECUTED.value, AEDConstants.AED_NODE_EXECUTED.value):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_INVALID_ARGUMENT, "(_aed_update_node_state)", "nodestate",
                                     [AEDConstants.AED_NODE_NOT_EXECUTED.value, AEDConstants.AED_NODE_EXECUTED.value]),
                MessageCodes.AED_INVALID_ARGUMENT)

        try:
            # *** AED request to update single node state
            self.aed_context.ele_common_lib.aed_update_node_state_single(self.aed_context._arr_c([nodeid]),
                                                                  c_int(nodestate), ret_code)
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_update_node_state_single)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0])

    def _print_dag(self):
        """
        This wrapper function facilitates a integration with 'print_dag',
        a C++ function, in AED library, with Python tdml library.

        To get all node contents and print the same.

        PARAMETERS:
            None

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            AedObj._print_dag()

        RETURNS:
            None

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED
        """
        # TODO:: Needs support from AED to accept node to be printed.
        # Specify the argument types
        self.aed_context.ele_common_lib.print_dag.argtypes = []

        try:
            # *** AED request to generate DAG path
            self.aed_context.ele_common_lib.print_dag()
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(print_dag)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

    def _print_dag_path(self, nodeid):
        """
        This wrapper function facilitates a integration with 'print_dag_path',
        a C++ function, in AED library, with Python tdml library.

        Function to print complete node path for a DAG, from given nodeid.

        PARAMETERS:
            nodeid - A DAG node ID.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            AedObj._print_dag_path(aed_select_nodeid)

        RETURNS:
            None

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.print_dag_path.argtypes = [POINTER(c_char_p)]

        try:
            # *** AED request to print DAG path
            self.aed_context.ele_common_lib.print_dag_path(self.aed_context._arr_c([nodeid]))
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(print_dag_path)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

    def _aed_is_node_executed(self, nodeid):
        """
        This wrapper function facilitates a integration with 'aed_is_node_executed',
        a C++ function, in AED library, with Python tdml library.

        Function to check whether node is already executed or not.

        PARAMETERS:
            nodeid - A DAG node ID.

        RETURNS:
            True if node is executed, false if not executed.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            node_flag = AedObj._aed_is_node_executed(aed_select_nodeid) # Returns false.
            # Let's mark node as executed.
            num_nodes_updated = AedObj._aed_update_node_state(self, nodeid)
            node_flag = AedObj._aed_is_node_executed(aed_select_nodeid) # Returns True.

        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_is_node_executed.argtypes = [POINTER(c_char_p),
                                                                         POINTER(c_int),
                                                                         POINTER(c_int)]

        node_flag = self.aed_context._int_array1(0)
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request to check whether node is executed or not.
            self.aed_context.ele_common_lib.aed_is_node_executed(self.aed_context._arr_c([nodeid]),
                                                                 node_flag,
                                                                 ret_code
                                                                 )
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_is_node_executed)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

        node_executed = True
        if node_flag[0] == AEDConstants.AED_NODE_NOT_EXECUTED.value:
            node_executed = False

        return self.aed_context._validate_aed_return_code(ret_code[0], node_executed)

    def _aed_get_tablename(self, nodeid):
        """
        This wrapper function facilitates a integration with 'aed_get_tablename',
        a C++ function, in AED library, with Python tdml library.

        Function to get table name for the provided node id..

        PARAMETERS:
            nodeid - A DAG node ID.

        RETURNS:
            Fully qualified table name. (dbname.tablename)

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            table_name = AedObj._aed_get_table(aed_table_nodeid).

        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_get_tablename.argtypes = [POINTER(c_char_p),
                                                                      POINTER(c_char_p),
                                                                      POINTER(c_char_p),
                                                                      POINTER(c_int)]
        outstr = "0" * AEDConstants.AED_DB_OBJECT_NAME_BUFFER_SIZE.value
        output_table = self.aed_context._arr_c([outstr])
        output_schema = self.aed_context._arr_c([outstr])
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request to get table name from node id.
            self.aed_context.ele_common_lib.aed_get_tablename(self.aed_context._arr_c([nodeid]),
                                                              output_table,
                                                              output_schema,
                                                              ret_code
                                                              )

            tablename = UtilFuncs._teradata_quote_arg(output_table[0].decode('UTF-8'), "\"")
            if output_schema[0].decode('UTF-8') != outstr and len(output_schema[0]) != 0:
                tablename = "{}.{}".format(UtilFuncs._teradata_quote_arg(output_schema[0].decode('UTF-8'), "\""),
                                           tablename)
            del outstr
            del output_schema
            del output_table
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_get_tablename)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], tablename)

    def _aed_orderby(self, nodeid, orderby_expr):
        """
        This wrapper function facilitates a integration with 'aed_orderby',
        a C++ function, in AED library, with Python tdml library.

        This function must be called when a ORDERBY operation that is
        columns are to be ordered from a Python (tdml) data frame.

        PARAMETERS:
            nodeid - A DAG node, a input to the orderby API.
            orderby_expr - orderby expression.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_orderby(aed_table_nodeid, "col1 ASC, col2 DESC")

        RETURNS:
            A node id in DAG - AED orderby API.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_orderby.argtypes =[POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_int)
                                                  ]

        arg_name = ["orderby"]
        arg_value = [orderby_expr]
        temp_table_name = UtilFuncs._generate_temp_table_name(prefix="orderby_", use_default_database=True, quote=False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]

        # Output nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])
        # return code
        ret_code = self.aed_context._int_array1(0)
        try:
            # *** AED request to select columns
            self.aed_context.ele_common_lib.aed_orderby(self.aed_context._arr_c([nodeid]),
                                           self.aed_context._arr_c(arg_name),
                                           self.aed_context._arr_c(arg_value),
                                           self.aed_context._arr_c(output_table),
                                           self.aed_context._arr_c(output_schema),
                                           nodeid_out,
                                           ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_orderby)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))

    def _aed_join(self, left_nodeid, right_nodeid, select_expr, join_type, join_condition, l_alias=None, r_alias=None):
        """
        This wrapper function facilitates a integration with 'aed_join',
        a C++ function, in AED library, with Python tdml library.

        This function must be called when a JOIN operation that is
        two Python (tdml) data frames to be joined on a condition.

        PARAMETERS:
            left_nodeid    - A DAG node, left table to be join.
            right_nodeid   - A DAG node, right table to be join.
            select_expr    - Columns to select after performing join.
            join_type      - Type of join to perform on two tables.
            join_condition - Join condition to perform JOIN on two tables.
            l_alias        - Alias name to be added to left table.
            r_alias        - Alias name to be added to right table.


        EXAMPLES:
            aed_table1_nodeid = AedObj._aed_table("dbname.tablename1")
            aed_table2_nodeid = AedObj._aed_table("dbname.tablename2")
            aed_join_nodeid = self.aed_obj._aed_join(filter_node_id1, select_node_id1,
                                           "df1.col1 as df1_col1, df2.col1 as df2_col1, df1.col2,df2.col3",
                                           "inner",  "df1.col1 = df2.col1 and df1.col2 = df2.col3", "df1", "df2")

        RETURNS:
            A node id in DAG - AED join API.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_join.argtypes =[POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_int)
                                                  ]

        arg_name = [join_type, l_alias, r_alias, "projection"]
        arg_value = [join_condition, l_alias, r_alias, select_expr]
        temp_table_name = UtilFuncs._generate_temp_table_name(prefix="join_", use_default_database=True, quote=False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]

        # Output nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])
        # return code
        ret_code = self.aed_context._int_array1(0)
        try:
            # *** AED request to select columns
            self.aed_context.ele_common_lib.aed_join(self.aed_context._arr_c([left_nodeid,right_nodeid]),
                                           self.aed_context._arr_c(arg_name),
                                           self.aed_context._arr_c(arg_value),
                                           self.aed_context._arr_c(output_table),
                                           self.aed_context._arr_c(output_schema),
                                           nodeid_out,
                                           ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_join)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))

    def _aed_assign(self, nodeid, assign_expr,
                    drop_existing_columns = AEDConstants.AED_ASSIGN_DO_NOT_DROP_EXISITING_COLUMNS.value):
        """
        This wrapper function facilitates a integration with 'aed_assign',
        a C++ function, in AED library, with Python tdml library.

        This function must be called when evaluating SQL expressions.

        PARAMETERS:
            nodeid - A DAG node, a input to the aed_assign API.
            assign_expr - SQL expression to evaluate.
            drop_existing_columns - Whether to drop exisitng columns or not.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_assign_nodeid = AedObj._aed_assign(aed_table_nodeid,
                                                   "abs(col1) as abs_col1, upper(col2) as upper_col2", "Y")

        RETURNS:
            A node id in DAG - AED assign API.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED, AED_NON_ZERO_STATUS and AED_INVALID_ARGUMENT
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_assign.argtypes = [POINTER(c_char_p),
                                                                POINTER(c_char_p),
                                                                POINTER(c_char_p),
                                                                POINTER(c_char_p),
                                                                POINTER(c_char_p),
                                                                POINTER(c_char_p),
                                                                POINTER(c_int)
                                                                ]
        if drop_existing_columns not in (AEDConstants.AED_ASSIGN_DROP_EXISITING_COLUMNS.value,
                                         AEDConstants.AED_ASSIGN_DO_NOT_DROP_EXISITING_COLUMNS.value):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_INVALID_ARGUMENT, "(_aed_assign)", "drop_existing_columns",
                                     [AEDConstants.AED_ASSIGN_DROP_EXISITING_COLUMNS.value,
                                      AEDConstants.AED_ASSIGN_DO_NOT_DROP_EXISITING_COLUMNS.value]),
                MessageCodes.AED_INVALID_ARGUMENT)

        arg_name = ["assign", "drop_cols"]
        arg_value = [assign_expr, drop_existing_columns]
        temp_table_name = UtilFuncs._generate_temp_table_name(prefix="assign_", use_default_database=True, quote=False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]

        # Output nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])
        # return code
        ret_code = self.aed_context._int_array1(0)
        try:
            # *** AED request to evaluate sql expressions
            self.aed_context.ele_common_lib.aed_assign(self.aed_context._arr_c([nodeid]),
                                                        self.aed_context._arr_c(arg_name),
                                                        self.aed_context._arr_c(arg_value),
                                                        self.aed_context._arr_c(output_table),
                                                        self.aed_context._arr_c(output_schema),
                                                        nodeid_out,
                                                        ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_assign)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))

    def _aed_get_node_query_type(self, nodeid):
        """
        This wrapper function facilitates a integration with 'aed_get_node_query_type',
        a C++ function, in AED library, with Python tdml library.

        Function to get type of provided node id.

        PARAMETERS:
            nodeid - A DAG node ID.

        RETURNS:
            Node query type.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            node_type = AedObj._aed_get_node_query_type(aed_table_nodeid).

        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_get_node_query_type.argtypes = [POINTER(c_char_p),
                                                                      POINTER(c_char_p),
                                                                      POINTER(c_int)]
        outstr = "0" * AEDConstants.AED_NODE_TYPE_BUFFER_SIZE.value
        node_type_buf = self.aed_context._arr_c(outstr)
        ret_code = self.aed_context._int_array1(0)

        try:
            # *** AED request to get type of the node id.
            self.aed_context.ele_common_lib.aed_get_node_query_type(self.aed_context._arr_c([nodeid]),
                                                              node_type_buf,
                                                              ret_code
                                                              )
            node_type = node_type_buf[0].decode('UTF-8')
            del node_type_buf
        except Exception as emsg:
            raise TeradataMlException(
                Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_get_node_query_type)" + str(emsg)),
                MessageCodes.AED_EXEC_FAILED)

        return self.aed_context._validate_aed_return_code(ret_code[0], node_type)
    
    def _aed_groupby(self, nodeid, groupby_expr):
        """
        This wrapper function facilitates a integration with 'aed_groupby',
        a C++ function, in AED library, with Python tdml library.

        This function must be called when a GROUP BY operation for specific
        columns are to be selected from a Python (tdml) data frame.

        PARAMETERS:
            nodeid - A DAG node, a input to the select API.
            groupby_expr - Columns, to be given from the data frame.

        EXAMPLES:
            aed_table_nodeid = AedObj._aed_table("dbname.tablename")
            aed_select_nodeid = AedObj._aed_select(aed_table_nodeid, "col1, col2, col3")
            aed_groupby_nodeid = AedObj._aed_groupby(aed_select_nodeid, "col1, col2, col3")

        RETURNS:
            A node id in DAG - AED group_by API.

        RAISES:
             Teradataml exceptions:
                AED_EXEC_FAILED and AED_NON_ZERO_STATUS        
        """
        # Specify the argument types
        self.aed_context.ele_common_lib.aed_groupby.argtypes =[POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_char_p),
                                                  POINTER(c_int)
                                                  ]

        arg_name = ["group by"]
        arg_value = [groupby_expr]
        temp_table_name = UtilFuncs._generate_temp_table_name(prefix="groupby_", use_default_database=True, quote=False)
        output_table = [UtilFuncs._extract_table_name(temp_table_name)]
        output_schema = [UtilFuncs._extract_db_name(temp_table_name)]

        # Output nodeid
        nodeid_out = self.aed_context._arr_c(["00000000000000000000"])

        # return code
        ret_code = self.aed_context._int_array1(0)
        try:
            # *** AED request to group by
            self.aed_context.ele_common_lib.aed_groupby(self.aed_context._arr_c([nodeid]),
                                           self.aed_context._arr_c(arg_name),
                                           self.aed_context._arr_c(arg_value),
                                           self.aed_context._arr_c(output_table),
                                           self.aed_context._arr_c(output_schema),
                                           nodeid_out,
                                           ret_code)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, "(aed_groupby)" + str(emsg)),
                                      MessageCodes.AED_EXEC_FAILED)
    
        return self.aed_context._validate_aed_return_code(ret_code[0], nodeid_out[0].decode("utf-8"))