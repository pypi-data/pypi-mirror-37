#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Kotha Mounika (mounika.kotha@teradata.com)
# 
# Version: 1.2
# Function Version: 1.2
# 
# ################################################################## 

from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.context.context import *
from teradataml.dataframe.dataframe import DataFrame
from teradataml.common.aed_utils import AedUtils
from teradataml.analytics.analytic_query_generator import AnalyticQueryGenerator
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.options.display import display

class TF:
    
    def __init__(self,
        data = None,
        formula = "normal",
        data_sequence_column = None,
        data_partition_column = None) :
        """
        DESCRIPTION:
             TF (Term Frequency) is used in conjuction with function TF-IDF 
             (Term Frequency - Inverse Document Frequency).
             TF-IDF is a technique for weighting words in a document. The 
             resulting weights can be used together in a vector space model as
             input for various document clustering or classification algorithms.
             
             To compute TF-IDF values, the TF_IDF function relies on the TF 
             function, which computes the TF value of the input.
        
        
        PARAMETERS:
            data:
                Required Argument.
                The input TeradataML DataFrame that contains the document id and the 
                term.
            
            data_partition_column:
                Required Argument.
                Partition By columns for data.
                Values to this argument can be provided as list, if multiple columns 
                are used for ordering.
            
            formula:
                Optional Argument.
                Specifies the formula for calculating the term frequency (tf) of term 
                t in document d: 
                    • normal: Normalized frequency (default): 
                      tf (t, d) = f ((t, d) / sum { w,w ? d }. This value is rf 
                      divided by the number of terms in the document. 
                    • bool: Boolean frequency: tf ((t, d) = 1 if t occurs in d; 
                      otherwise, tf ((t, d) = 0. 
                    • log: Logarithmically-scaled frequency: 
                      tf ((t, d) = log (f ((t, d) + 1) where f ((t, d) is the
                      number of times t occurs in d (that is, the raw frequency, 
                      rf). 
                    • augment: Augmented frequency (to prevent bias towards 
                      longer documents): tf ((t, d) = 0.5 + (0.5 × f ((t, d) / 
                      max { f (w, d) : w ? d }). This value is rf divided by 
                      the maximum raw frequency of any term in the document. 
                      
                Note: When using the output of a previous run of the tf_idf 
                function on a training document set to predict ta.tf_idf scores
                on an input document set, use the same "formula" value for the
                input document set that you used for the training document set.
                Default Value: "normal"
                Permitted Values: bool, log, augment, normal
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
        
        RETURNS:
            Instance of TF.
            Output TeradataML DataFrames can be accessed using attribute
            references, such as TFObj.<attribute_name>.
            Output TeradataML DataFrame attribute name is:
                result
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
           # Create TeradataML DataFrame.
            tfidf_input1 = DataFrame.from_table("tfidf_input1")
            
            # Example 1 -
            tf_result = TF(data=tfidf_input1_view,
                        data_partition_column='docid',
                        formula='normal',
                        data_sequence_column='docid'
                        )
            # Print the result DataFrame
            tf_result.result
        
        """
        self.data  = data 
        self.formula  = formula 
        self.data_sequence_column  = data_sequence_column 
        self.data_partition_column  = data_partition_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, "DataFrame"])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, "str"])
        self.__arg_info_matrix.append(["formula", self.formula, True, "str"])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, "str"])
        
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
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        
        # Check for permitted values
        formula_permitted_values = ["BOOL", "LOG", "AUGMENT", "NORMAL"]
        self.__awu._validate_permitted_values(self.formula, formula_permitted_values, "formula")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data")
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data")
        
        
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
        
        if self.formula is not None and self.formula != "normal":
            self.__func_other_arg_sql_names.append("Formula")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.formula,"'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column,""))
        
        if len(sequence_input_by_list) > 0:
            self.__func_other_arg_sql_names.append("SequenceInputBy")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(sequence_input_by_list,"'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column,"\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(data_partition_column)
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "TF"
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
        
        # Print SQL-MR query if requested to do so.
        if display.print_sqlmr_query:
            print(self.sqlmr_query)
        
    def __execute(self) :
        """
        Function to execute SQL-MR queries. 
        Creates dataframes for the required SQL-MR outputs.
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
        Returns the string representation for a TF class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
