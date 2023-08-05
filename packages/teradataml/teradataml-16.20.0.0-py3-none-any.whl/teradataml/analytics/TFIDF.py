#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# 
# Version: 1.2
# Function Version: 2.3
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
from teradataml.analytics.TF import TF

class TFIDF:
    
    def __init__(self,
        object = None,
        doccount_data = None,
        docperterm_data = None,
        idf_data = None,
        object_partition_column = None,
        docperterm_data_partition_column = None,
        idf_data_partition_column = None) :
        """
        DESCRIPTION:
            TF_IDF evaluates the importance of a word within a specific document, 
            weighted by the number of times the word appears in the entire 
            corpus of documents. Term frequency(tf) indicates how often a term 
            appears in a specific document. Inverse document frequency(idf) 
            measures the general importance of a term within an entire corpus 
            of documents. That is, each term in the dictionary has an idf score. 
            Each term in each document is given a TF_IDF score, which is 
            equal to tf * idf. A high TF_IDF score for a term generally means 
            that the term is uniquely relevant to a specific document. To 
            compute TF_IDF score, the TF_IDF SQL-MR function relies on the 
            TF SQL-MR function, which computes the term frequency value of the 
            input.
        
        PARAMETERS:
            object:
                Required Argument.
                Specifies the TeradataML DataFrame that contains the tf values.
            
            object_partition_column:
                Required Argument.
                Partition By columns for object.
                Values to this argument can be provided as list, if multiple 
                columns are used for partition.
            
            doccount_data:
                Optional Argument.
                Specifies the TeradataML DataFrame that contains the total 
                number of documents.
            
            docperterm_data:
                Optional Argument.
                Specifies the TeradataML DataFrame that contains the total 
                number of documents that each term appears.
            
            docperterm_data_partition_column:
                Optional Argument.
                Partition By columns for docperterm_data.
                Values to this argument can be provided as list, if multiple 
                columns are used for partition.
            
            idf_data:
                Optional Argument.
                Specifies the TeradataML DataFrame that contains the idf values
                that the predict process outputs.
            
            idf_data_partition_column:
                Optional Argument.
                Partition By columns for idf_data.
                Values to this argument can be provided as list, if multiple
                columns are used for partition.
        
        RETURNS:
            Instance of TFIDF.
            Output TeradataML DataFrames can be accessed using attribute
            references, such as TFIDFObj.<attribute_name>.
            Output TeradataML DataFrame attribute name is:
                result
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
            # Create TeradataML DataFrame.
            tfidf_train = DataFrame.from_table("tfidf_train")
            docperterm_table = DataFrame.from_table("docperterm_table")
            tfidf_doccount = DataFrame.from_table("dccount_table")
            dccount_table2 = DataFrame.from_table("dccount_table2")
            idf_tbl =  DataFrame.from_query("select distinct token , idf from tf_idf_train_output")
            
            #Create tf output to be used in TFIDF functions
            tf_table = TF(data = tfidf_train,
                    data_sequence_column = "id",
                    data_partition_column = "id")

            # Example 1 -
            tfidf_result1 = TFIDF(object = tf_table,
                    doccount_data = tfidf_doccount,
                    object_partition_column = 'token')
            
            # Print the result DataFrame
            tfidf_result1.result
            
            #Example 2 -
            tfidf_result2 = TFIDF(object = tf_table,
                    docperterm_data = docperterm_table,
                    idf_data = idf_tbl,
                    object_partition_column = 'token',
                    docperterm_data_partition_column = 'term',
                    idf_data_partition_column = 'token')
            
            # Print the result DataFrame
            tfidf_result2.result

        """
        self.object  = object 
        self.doccount_data  = doccount_data 
        self.docperterm_data  = docperterm_data 
        self.idf_data  = idf_data 
        self.object_partition_column  = object_partition_column 
        self.docperterm_data_partition_column  = docperterm_data_partition_column 
        self.idf_data_partition_column  = idf_data_partition_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, "DataFrame"])
        self.__arg_info_matrix.append(["object_partition_column", self.object_partition_column, False, "str"])
        self.__arg_info_matrix.append(["doccount_data", self.doccount_data, True, "DataFrame"])
        self.__arg_info_matrix.append(["docperterm_data", self.docperterm_data, True, "DataFrame"])
        self.__arg_info_matrix.append(["docperterm_data_partition_column", self.docperterm_data_partition_column, True, "str"])
        self.__arg_info_matrix.append(["idf_data", self.idf_data, True, "DataFrame"])
        self.__arg_info_matrix.append(["idf_data_partition_column", self.idf_data_partition_column, True, "str"])
        
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
        if isinstance(self.object, TF):
            self.object = self.object._mlresults[0]
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.object, "object", TF)
        self.__awu._validate_input_table_datatype(self.doccount_data, "doccount_data", None)
        self.__awu._validate_input_table_datatype(self.docperterm_data, "docperterm_data", None)
        self.__awu._validate_input_table_datatype(self.idf_data, "idf_data", None)
        
        self.__awu._validate_input_columns_not_empty(self.object_partition_column, "object_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_partition_column, "object_partition_column", self.object, "object")
        
        self.__awu._validate_input_columns_not_empty(self.docperterm_data_partition_column, "docperterm_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.docperterm_data_partition_column, "docperterm_data_partition_column", self.docperterm_data, "docperterm_data")
        
        self.__awu._validate_input_columns_not_empty(self.idf_data_partition_column, "idf_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.idf_data_partition_column, "idf_data_partition_column", self.idf_data, "idf_data")
        
        
    def __form_tdml_query(self) :
        """
        Function to generate the analaytical function queries. The function defines variables and list of arguments required to form the query.
        """
        
        # Output table arguments list
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process object
        object_partition_column = UtilFuncs._teradata_collapse_arglist(self.object_partition_column,"\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("tf")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(object_partition_column)
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Process doccount_data
        if self.doccount_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.doccount_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("doccount")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        # Process docperterm_data
        if self.docperterm_data is not None:
            docperterm_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.docperterm_data_partition_column,"\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.docperterm_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("docperterm")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(docperterm_data_partition_column)
            self.__func_input_order_by_cols.append("NA_character_")
        
        # Process idf_data
        if self.idf_data is not None:
            idf_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.idf_data_partition_column,"\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.idf_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("idf")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(idf_data_partition_column)
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "TFIDF"
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
        Creates DataFrames for the required SQL-MR outputs.
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
        Returns the string representation for a TFIDF class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
