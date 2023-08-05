#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Karthik Thelukuntla (karthik.thelukuntla@teradata.com)
# 
# Version: 1.2
# Function Version: 1.1
# 
# ################################################################## 

from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.common.aed_utils import AedUtils
from teradataml.analytics.analytic_query_generator import AnalyticQueryGenerator
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.options.display import display

class NPath:
    
    def __init__(self,
        data1 = None,
        mode = None,
        pattern = None,
        symbols = None,
        result = None,
        filter = None,
        data2 = None,
        data3 = None,
        data1_partition_column = None,
        data2_partition_column = None,
        data3_partition_column = None,
        data1_order_column = None,
        data2_order_column = None,
        data3_order_column = None) :
        """
        DESCRIPTION:
            The nPath function scans a set of rows, looking for patterns that you 
            specify. For each set of input rows that matches the pattern, nPath 
            produces a single output row. The function provides a flexible 
            pattern-matching capability that lets you specify complex patterns in 
            the input data and define the values that are output for each matched 
            input set.
        
        
        PARAMETERS:
            data1:
                Required Argument.
                Specifies the input TeradataML DataFrame containing the input data set.
            
            data1_partition_column:
                Required Argument.
                Partition By columns for data1.
                Values to this argument can be provided as list, if multiple columns 
                are used for partition.
            
            data1_order_column:
                Required Argument.
                Order By columns for data1.
                Values to this argument can be provided as list, if multiple columns 
                are used for ordering.
            
            mode:
                Required Argument.
                Specifies the pattern-matching mode: 
                OVERLAPPING: The function finds every occurrence of the pattern in
                             the partition, regardless of  whether it is part of a previously
                             found match. Therefore, one row can match multiple symbols in a
                             given matched pattern.
                NONOVERLAPPING: The function begins the next pattern search at the
                                row that follows the last  pattern match. This is the default
                                behavior of many commonly used pattern matching utilities, including
                                the UNIX grep utility.
                Permitted Values: OVERLAPPING, NONOVERLAPPING
            
            pattern:
                Required Argument.
                Specifies the pattern for which the function searches. You compose 
                pattern with the symbols that you define in the symbols argument, 
                operators, and parentheses. TeradataML DataFrame describes the 
                simplest patterns, which you can combine to form more complex 
                patterns. When patterns have multiple operators, the function applies 
                them in order of precedence, and applies operators of equal 
                precedence from left to right. TeradataML DataFrame also shows 
                operator precedence. To force the function to evaluate a subpattern 
                first, enclose it in parentheses. To specify that a subpattern must 
                appear a specific number of times, use the ?Range-Matching 
                Feature??.
                 For pattern matching details, refer to ?Pattern Matching??.
            
            symbols:
                Required Argument.
                Defines the symbols that appear in the values of the pattern and 
                result arguments. The col_expr is an expression whose value is a 
                column name, symbol is any valid identifier, and  symbol_predicate is 
                a SQL predicate (often a column name).
                 For example, the Symbols argument for analyzing website visits might 
                look like this: 
                symbols 
                (
                 pagetype = "homepage" AS H, 
                pagetype <> "homepage" AND  pagetype <> "checkout" AS PP,
                 pagetype = "checkout" AS CO 
                )
                 The symbol is case-insensitive; however, a symbol of one or two 
                uppercase letters is easy to identify in patterns. 
                If col_expr represents a column that appears in multiple input 
                tables, then you must qualify the ambiguous column name with its 
                TeradataML DataFrame name. For example: 
                 Symbols 
                 ( 
                 weblog.pagetype = "homepage" AS H, 
                 weblog.pagetype = "thankyou" AS T, 
                 ads.adname = "xmaspromo" AS X, 
                 ads.adname = "realtorpromo" AS R 
                ) 
                For more information about symbols that appear in the Pattern 
                argument value, refer to ?symbols??. For more information about 
                symbols that appear in the Result argument value, refer to ?result: 
                Applying Aggregate Functions??.
            
            result:
                Required Argument.
                Defines the output columns. The col_expr is an expression whose value 
                is a column name; it specifies the values to retrieve from the 
                matched rows. The function applies aggregate_function  to these 
                values. For details, see ?result: Applying Aggregate Functions??. 
                The function evaluates this argument once for every matched pattern 
                in the partition (that is, it outputs one row for each pattern match).
            
            filter:
                Optional Argument.
                Specifies filters to impose on the matched rows. The function 
                combines the filter expressions using the AND operator. 
                The filter_expression syntax is: 
                symbol_expression  comparison_operator symbol_expression 
                The two symbol expressions must be type-compatible. The 
                symbol_expression syntax is: 
                { FIRST | LAST }(column_with_expression OF [ANY](symbol[,...])) 
                The column_with_expression cannot contain the operator AND or OR, and 
                all its columns must come from the same input. If the function has 
                multiple inputs, then column_with_expression and symbol must come 
                from the same input. 
                The comparison_operator is either <, >, <=, >=, =, or <>.
            
            data2:
                Optional Argument.
                Specifies the additional optional input TeradataML DataFrame containing the input data set.
            
            data2_partition_column:
                Optional Argument.
                Partition By columns for data2.
                Values to this argument can be provided as list, if multiple columns 
                are used for Partition.
            
            data2_order_column:
                Optional Argument.
                Order By columns for data2.
                Values to this argument can be provided as list, if multiple columns 
                are used for ordering.
            
            data3:
                Optional Argument.
                Specifies the additional optional input TeradataML DataFrame containing the input data set.
            
            data3_partition_column:
                Optional Argument.
                Partition By columns for data3.
                Values to this argument can be provided as list, if multiple columns 
                are used for Partition.
            
            data3_order_column:
                Optional Argument.
                Order By columns for data3.
                Values to this argument can be provided as list, if multiple columns 
                are used for ordering.
        
        RETURNS:
            Instance of NPath.
            Output TeradataML DataFrames can be accessed using attribute
            references, such as NPathObj.<attribute_name>.
            Output TeradataML DataFrame attribute name is:
                result
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
            # Create input TeradataML dataframes
            impressions = DataFrame.from_table("impressions")
            clicks2 = DataFrame.from_table("clicks2")
            tv_spots = DataFrame.from_table("tv_spots")

            # Run NPath function
            result = NPath(data1=impressions,
            data1_partition_column='userid',
            data1_order_column='ts',
            data2=clicks2,
            data2_partition_column='userid',
            data2_order_column='ts',
            data3=tv_spots,
            data3_partition_column='ts',
            data3_order_column='ts',
            result=['COUNT(* of imp) as imp_cnt','COUNT(* of imp) as imp_cnt_1'],
            mode='nonoverlapping',
            pattern='(imp|tv_imp)*.click',
            symbols=['true as imp','true as click','true as tv_imp']
            )
            # Print output dataframe.
            print(result.result)

        """
        self.data1  = data1 
        self.mode  = mode 
        self.pattern  = pattern 
        self.symbols  = symbols 
        self.result  = result 
        self.filter  = filter 
        self.data2  = data2 
        self.data3  = data3 
        self.data1_partition_column  = data1_partition_column 
        self.data2_partition_column  = data2_partition_column 
        self.data3_partition_column  = data3_partition_column 
        self.data1_order_column  = data1_order_column 
        self.data2_order_column  = data2_order_column 
        self.data3_order_column  = data3_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data1", self.data1, False, "DataFrame"])
        self.__arg_info_matrix.append(["data1_partition_column", self.data1_partition_column, False, "str"])
        self.__arg_info_matrix.append(["data1_order_column", self.data1_order_column, False, "str"])
        self.__arg_info_matrix.append(["mode", self.mode, False, "str"])
        self.__arg_info_matrix.append(["pattern", self.pattern, False, "str"])
        self.__arg_info_matrix.append(["symbols", self.symbols, False, "str"])
        self.__arg_info_matrix.append(["result", self.result, False, "str"])
        self.__arg_info_matrix.append(["filter", self.filter, True, "str"])
        self.__arg_info_matrix.append(["data2", self.data2, True, "DataFrame"])
        self.__arg_info_matrix.append(["data2_partition_column", self.data2_partition_column, True, "str"])
        self.__arg_info_matrix.append(["data2_order_column", self.data2_order_column, True, "str"])
        self.__arg_info_matrix.append(["data3", self.data3, True, "DataFrame"])
        self.__arg_info_matrix.append(["data3_partition_column", self.data3_partition_column, True, "str"])
        self.__arg_info_matrix.append(["data3_order_column", self.data3_order_column, True, "str"])
        
        # Perform the function validations
        self.__validate()
        # Generate the ML query
        self.__form_tdml_query()
        # Execute ML query
        self.__execute()
        
    def __validate(self) :
        """
        Function to validate sqlmr function arguments to verify missing 
        arguments, input argument and table types. Also processes the 
        argument values.
        """
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data1, "data1", None)
        self.__awu._validate_input_table_datatype(self.data2, "data2", None)
        self.__awu._validate_input_table_datatype(self.data3, "data3", None)
        
        # Check for permitted values
        mode_permitted_values = ["OVERLAPPING", "NONOVERLAPPING"]
        self.__awu._validate_permitted_values(self.mode, mode_permitted_values, "mode")
        
        self.__awu._validate_input_columns_not_empty(self.data1_partition_column, "data1_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data1_partition_column, "data1_partition_column", self.data1, "data1")
        
        self.__awu._validate_input_columns_not_empty(self.data2_partition_column, "data2_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data2_partition_column, "data2_partition_column", self.data2, "data2")
        
        self.__awu._validate_input_columns_not_empty(self.data3_partition_column, "data3_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data3_partition_column, "data3_partition_column", self.data3, "data3")
        
        self.__awu._validate_input_columns_not_empty(self.data1_order_column, "data1_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data1_order_column, "data1_order_column", self.data1, "data1")
        
        self.__awu._validate_input_columns_not_empty(self.data2_order_column, "data2_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data2_order_column, "data2_order_column", self.data2, "data2")
        
        self.__awu._validate_input_columns_not_empty(self.data3_order_column, "data3_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data3_order_column, "data3_order_column", self.data3, "data3")
        
    def __form_tdml_query(self) :
        """
        Function to generate the analytical function queries. The function defines variables and list of arguments required to form the query.
        """
        
        # Output table arguments list
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("Mode")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mode,""))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("Pattern")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.pattern,"'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("Symbols")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.symbols,""))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.filter is not None:
            self.__func_other_arg_sql_names.append("Filter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.filter,""))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("Result")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.result,""))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data1
        data1_partition_column = UtilFuncs._teradata_collapse_arglist(self.data1_partition_column,"\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data1, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input1")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(data1_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data1_order_column,"\""))
        
        # Process data2
        if self.data2 is not None:
            data2_distribution = "DIMENSION"
            if self.data2_partition_column is not None:
                data2_distribution = "FACT"
                data2_partition_column = UtilFuncs._teradata_collapse_arglist(self.data2_partition_column,"\"")
            else:
                data2_partition_column = "NA_character_"
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data2, False)
            self.__func_input_distribution.append(data2_distribution)
            self.__func_input_arg_sql_names.append("input2")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(data2_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data2_order_column,"\""))
        
        # Process data3
        if self.data3 is not None:
            data3_distribution = "DIMENSION"
            if self.data3_partition_column is not None:
                data3_distribution = "FACT"
                data3_partition_column = UtilFuncs._teradata_collapse_arglist(self.data3_partition_column,"\"")
            else:
                data3_partition_column = "NA_character_"
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data3, False)
            self.__func_input_distribution.append(data3_distribution)
            self.__func_input_arg_sql_names.append("input3")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(data3_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data3_order_column,"\""))
        
        function_name = "nPath"
        # Create instance to generate SQLMR.
        aqg_obj = AnalyticQueryGenerator(function_name 
                ,self.__func_input_arg_sql_names 
                ,self.__func_input_table_view_query 
                ,self.__func_input_dataframe_type 
                ,self.__func_input_distribution 
                ,self.__func_input_partition_by_cols 
                ,self.__func_input_order_by_cols 
                ,self.__func_other_arg_sql_names 
                ,self.__func_other_args 
                ,self.__func_other_arg_json_datatypes 
                ,self.__func_output_args_sql_names 
                ,self.__func_output_args)
        # Invoke call to SQL-MR generation.
        self.sqlmr_query = aqg_obj._gen_sqlmr_select_stmt_sql()
        
        #Print SQL-MR query if requested to do so.
        if display.print_sqlmr_query:
            print(self.sqlmr_query)
        
    def __execute(self) :
        """
        Function to execute SQL-MR queries. 
        And creates dataframes for the required SQL-MR outputs.
        """
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix = "td_sqlmr_out_", use_default_database = True, gc_on_quit = True, quote=False)
        try:
            UtilFuncs._create_view(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.result)
        
    def __repr__(self) :
        """
        Returns the string representation for a NPath class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
