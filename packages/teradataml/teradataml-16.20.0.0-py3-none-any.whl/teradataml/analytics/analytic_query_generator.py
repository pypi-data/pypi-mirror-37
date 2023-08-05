#########################################################################
# Unpublished work.                                                     #
# Copyright (c) 2018 by Teradata Corporation. All rights reserved.      #
# TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET                    #
#                                                                       #
# Primary Owner: pankajvinod.purandare@teradata.com                     #
# Secondary Owner:                                                      #
#                                                                       #
# This file implements class creates a SQL-MR object, which can be      #
# used to generate SQL-MR/Analytical query in FFE syntax for Teradata.  #
#########################################################################

from teradataml.common.utils import UtilFuncs

class AnalyticQueryGenerator:
    """
    This class creates a SQL-MR object, which can be used to generate
    SQL-MR/Analytical query in FFE syntax for Teradata.
    """

    def __init__(self, function_name, func_input_arg_sql_names, func_input_table_view_query, func_input_dataframe_type,
                 func_input_distribution, func_input_partition_by_cols, func_input_order_by_cols,
                 func_other_arg_sql_names, func_other_args_values, func_other_arg_json_datatypes,
                 func_output_args_sql_names, func_output_args_values, func_type="FFE"):
        """
        AnalyticalQueryGenerator constructor, to create a map-reduce object, for
        SQL-MR/Analytical query generation.

        PARAMETERS:
            function_name - Name of the function.
            func_input_arg_sql_names - List of input SQL Argument names.
            func_input_table_view_query - List of input argument values, with respect to 'func_input_arg_sql_names'
                                            which contains table_name or SQL (Select query)
            func_input_dataframe_type - List of dataframe types for each input. Values can be "TABLE" or "QUERY".
            func_input_distribution - A List containing distributions for each input. Values can be "FACT", "DIMENSION", "NONE".
            func_input_partition_by cols - List containing partition columns for each input, if distribution is FACT.
            func_input_order_by_cols - List of values, for each input, to be used order by clause.
            func_other_arg_sql_names - List of other function arguments SQL name.
            func_other_args_values - List of other function argument values, with respect to each member in 'func_other_arg_sql_names'
            func_other_arg_json_datatypes - List of JSON datatypes for each member in 'func_other_arg_sql_names'
            func_output_args_sql_names - List of output SQL argument names.
            func_output_args_values - List of output table names for each output table argument in 'func_output_args_sql_names'.
            func_type - Fixed value 'FFE'. Kept for future purpose, to generate different syntaxes.

        RETURNS:
            AnalyticalQueryGenerator object. (We can call this as map-reduce object)

        RAISES:

        EXAMPLES:
            aqg_obj = AnalyticQueryGenerator(self.function_name, self.input_sql_args, self.input_table_qry,
                                         self.input_df_type,
                                         self.input_distribution, self.input_partition_columns,
                                         self.input_order_columns,
                                         self.other_sql_args, self.other_args_val, [], self.output_sql_args,
                                         self.output_args_val)
        """
        self.__function_name = function_name
        self.__func_input_arg_sql_names = func_input_arg_sql_names
        self.__func_input_table_view_query = func_input_table_view_query
        self.__func_input_dataframe_type = func_input_dataframe_type
        self.__func_input_distribution = func_input_distribution
        self.__func_input_partition_by_cols = func_input_partition_by_cols
        self.__func_input_order_by_cols = func_input_order_by_cols
        self.__func_other_arg_sql_names = func_other_arg_sql_names
        self.__func_other_args_values = func_other_args_values
        self.__func_other_arg_json_datatypes = func_other_arg_json_datatypes
        self.__func_output_args_sql_names = func_output_args_sql_names
        self.__func_output_args_values = func_output_args_values
        self.__func_type = func_type

    def __process_for_teradata_keyword(self, keyword):
        """
        Internal function to process Teradata Reserved keywords.
        If keyword is in list of Teradata Reserved keywords, then it'll be quoted in double quotes "keyword".

        PARAMETERS:
            keyword - A string to check whether it belongs to Teradata Reserved Keywords or not.

        RETURNS:
            A quoted string, if keyword is one of the Teradata Reserved Keyword, else str as is.

        RAISES:

        EXAMPLES:
            # Passing non-reserved returns "xyz" as is.
            keyword = self.__process_for_teradata_keyword("xyz")
            print(keyword)
            # Passing reserved str returns double-quoted str, i.e., "\"threshold\"".
            keyword = self.__process_for_teradata_keyword("threshold")
            print(keyword)

        """
        TERADATA_RESERVED_WORDS = ["INPUT", "THRESHOLD", "CHECK", "SUMMARY", "HASH", "METHOD"]
        if keyword.upper() in TERADATA_RESERVED_WORDS:
            return UtilFuncs._teradata_quote_arg(keyword, "\"")
        else:
            return keyword

    def __generate_sqlmr_func_other_arg_sql(self):
        """
        Private function to generate a SQL clause for other function arguments.
        For Example,
            Step("False")
            Family("BINOMIAL")

        PARAMETERS:

        RETURNS:
            SQL string for other function arguments, as shown in example here.

        RAISES:

        EXAMPLES:
            __func_other_arg_sql_names = ["Step", "Family"]
            __func_other_args_values = ["False", "BINOMIAL"]
            other_arg_sql = self.__generate_sqlmr_func_other_arg_sql()
            # Output is as shown in example in description.

        """
        args_sql_str = ""
        for index in range(len(self.__func_other_arg_sql_names)):
            args_sql_str = "{0}\n\t{1}({2})".format(args_sql_str,
                                                    self.__process_for_teradata_keyword(
                                                        self.__func_other_arg_sql_names[index]),
                                                    self.__func_other_args_values[index])
        return args_sql_str

    def __generate_sqlmr_input_arg_sql(self, table_ref, table_ref_type, alias=None):
        """
        Private function to generate a ON clause for input function arguments.
        For Example,
            ON table_name AS InputTable
            ON (select * from table) AS InputTable

        PARAMETERS:
            table_ref - Table name or query, to be used as input.
            table_ref_type - Type of data frame.
            alias - Alias to be used for input.

        RETURNS:
            ON clause SQL string for input function arguments, as shown in example here.

        RAISES:
            TODO

        EXAMPLES:
            other_arg_sql = self.__generate_sqlmr_input_arg_sql("table_name", "TABLE", "InputTable")
            # Output is as shown in example in description.

        """
        returnSql = "\n\tON"
        if table_ref_type == "TABLE":
            returnSql = "{0} {1}".format(returnSql, table_ref)
        elif table_ref_type == "QUERY":
            returnSql = "{0} ({1})".format(returnSql, table_ref)
        else:
            #TODO raise # Error
            ""

        if alias is not None:
            returnSql = "{0} AS {1}".format(returnSql, self.__process_for_teradata_keyword(alias))


        return returnSql

    def __generate_sqlmr_output_arg_sql(self):
        """
        Private function to generate a SQL clause for output function arguments.
        For Example,
            OUT TABLE OutputTable("out_table_1")
            OUT TABLE CoefficientsTable("out_table_2")

        PARAMETERS:

        RETURNS:
            SQL string for output function arguments, as shown in example here.

        RAISES:

        EXAMPLES:
            __func_output_args_sql_names = ["OutputTable", "CoefficientsTable"]
            __func_output_args_values = ["out_table_1", "out_table_2"]
            other_arg_sql = self.__generate_sqlmr_output_arg_sql()
            # Output is as shown in example in description.

        """
        args_sql_str = ""
        for index in range(len(self.__func_output_args_sql_names)):
            args_sql_str = "{0}\n\tOUT TABLE {1}({2})".format(args_sql_str,
                                                              self.__process_for_teradata_keyword(
                                                                  self.__func_output_args_sql_names[index]),
                                                              self.__func_output_args_values[index])
        return args_sql_str

    def _gen_sqlmr_select_stmt_sql(self):
        """
        Protected function to generate complete analytical query.
        For Example,
            SELECT * FROM GLM(
                input_arguments_clause
                output_arguments_clause
                USING
                other_arguments_clause
            ) as sqlmr

        PARAMETERS:

        RETURNS:
            A SQL-MR/Analytical query, as shown in example here.

        RAISES:

        EXAMPLES:
            aqg_obj = AnalyticQueryGenerator(self.function_name, self.input_sql_args, self.input_table_qry,
                                         self.input_df_type,
                                         self.input_distribution, self.input_partition_columns,
                                         self.input_order_columns,
                                         self.other_sql_args, self.other_args_val, [], self.output_sql_args,
                                         self.output_args_val)
            anly_query = aqg_obj._gen_sqlmr_select_stmt_sql()
            # Output is as shown in example in description.

        """
        return "SELECT * FROM {} as sqlmr".format(self._gen_sqlmr_invocation_sql())

    def _gen_sqlmr_invocation_sql(self):
        """
        Protected function to generate a part of analytical query, to be used for map-reduce functions.
        For Example,
            GLM(
                input_arguments_clause
                output_arguments_clause
                USING
                other_arguments_clause
            )

        PARAMETERS:

        RETURNS:
            A SQL-MR/Analytical query, as shown in example here.

        RAISES:

        EXAMPLES:
            aqg_obj = AnalyticQueryGenerator(self.function_name, self.input_sql_args, self.input_table_qry,
                                         self.input_df_type,
                                         self.input_distribution, self.input_partition_columns,
                                         self.input_order_columns,
                                         self.other_sql_args, self.other_args_val, [], self.output_sql_args,
                                         self.output_args_val)
            anly_query = aqg_obj._gen_sqlmr_invocation_sql()
            # Output is as shown in example in description.

        """
        invocation_sql = "{0}({1}{2}".format(self.__function_name, self.__single_complete_table_ref_clause(),
                                       self.__generate_sqlmr_output_arg_sql())

        if len(self.__func_other_arg_sql_names) != 0:
            invocation_sql = "{0}\n\tUSING{1}".format(invocation_sql, self.__generate_sqlmr_func_other_arg_sql())

        invocation_sql = invocation_sql + "\n)"

        return invocation_sql

    def __single_complete_table_ref_clause(self):
        """
        Private function to generate complete ON clause for input function arguments, including
        partition by and order by clause, if any.
        For Example,
            ON table_name AS InputTable1 Partition By col1 Order By col2
            ON (select * from table) AS InputTable2 DIMENSION

        PARAMETERS:

        RETURNS:
            Complete input argument clause, SQL string for input function arguments, as shown in example here.

        RAISES:

        EXAMPLES:
            __func_input_arg_sql_names = ["InputTable1", "InputTable2"]
            __func_input_table_view_query = ["table_name", "select * from table"]
            __func_input_dataframe_type = ["TABLE", "QUERY"]
            __func_input_distribution = ["FACT", "DIMENSION"]
            __func_input_partition_by_cols = ["col1", "NA_character_"]
            __func_input_order_by_cols = ["col2", "NA_character_"]
            other_arg_sql = self.__single_complete_table_ref_clause()
            # Output is as shown in example in description.

        """
        args_sql_str = ""
        for index in range(len(self.__func_input_arg_sql_names)):
            table_ref = self.__func_input_table_view_query[index]
            table_ref_type = self.__func_input_dataframe_type[index]
            alias = self.__func_input_arg_sql_names[index]
            distribution = self.__func_input_distribution[index]
            partition_col = self.__func_input_partition_by_cols[index]
            order_col = self.__func_input_order_by_cols[index]

            on_clause = self.__generate_sqlmr_input_arg_sql(table_ref, table_ref_type, alias)
            partition_clause = self.__gen_sqlmr_input_partition_clause(distribution, partition_col)
            order_clause = self.__gen_sqlmr_input_order_clause(order_col)

            args_sql_str = "{0}{1}{2}{3}".format(args_sql_str, on_clause, partition_clause, order_clause)

        return args_sql_str

    def __gen_sqlmr_input_order_clause(self, column_order):
        """
        Private function to generate complete order by clause for input function arguments.
        For Example,
            Order By col2

        PARAMETERS:
            column_order - Column to be used in ORDER BY clause. If this is "NA_character_"
                            no ORDER BY clause is generated.

        RETURNS:
            Order By clause, as shown in example here.

        RAISES:

        EXAMPLES:
            other_arg_sql = self.__gen_sqlmr_input_order_clause("col2")
            # Output is as shown in example in description.

        """
        if column_order == "NA_character_":
          return ""
        return "\n\tORDER BY {}".format(column_order)


    def __gen_sqlmr_input_partition_clause(self, distribution, column):
        """
        Private function to generate PARTITION BY or DIMENSION clause for input function arguments.
        For Example,
            Partition By col1
            DIMENSION

        PARAMETERS:
            distribution - Type of clause to be generated. Values accepted here are: FACT, DIMENSION, NONE
            column - Column to be used in PARTITION BY clause, when distribution is "FACT"

        RETURNS:
            Partition clause, based on the type of distribution:
                When "FACT" - PARTITION BY clause is generated.
                When "DIMENSION" - DIMENSION cluase is generated.
                When "NONE" - No clause is generated, an empty string is returned.

        RAISES:
            TODO

        EXAMPLES:
            other_arg_sql = self.__gen_sqlmr_input_partition_clause("FACT", "col1")
            # Output is as shown in example in description.

        """
        if distribution == "FACT" and column is not None:
            return "\n\tPARTITION BY {0}".format(column)
        elif distribution == "DIMENSION":
            return "\n\tDIMENSION"
        elif distribution == "NONE":
            return ""
        else:
            ""
            # TODO raise error "invalid distribution type"


