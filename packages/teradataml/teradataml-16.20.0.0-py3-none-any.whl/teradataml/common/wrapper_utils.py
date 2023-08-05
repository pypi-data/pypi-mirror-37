"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pankajvinod.purandare@teradata.com, mounika.kotha@teradata.com
Secondary Owner:

This file implements the core utilities those will be used by the Teradata Vantage
Analytic Function wrappers.
"""

import sys
import re
import inspect

from teradataml.common.utils import UtilFuncs
from teradataml.common.formula import Formula
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.messages import Messages
from teradataml.context.context import *
from teradataml.common.aed_utils import AedUtils
from teradataml.dataframe.dataframe_utils import DataFrameUtils
from teradataml.common.constants import SourceType
import teradataml.dataframe as tdmldf
from teradatasqlalchemy.types import INTEGER, SMALLINT, BIGINT, BYTEINT, FLOAT, NUMBER, VARCHAR

class AnalyticsWrapperUtils:

    def _deparse_arg_name(self,var):
        """
        Get the variable name of the calling funtcion's passed argument.
        PARAMETERS:
           var - The argument whose name has to be retrieved

        RETURNS:
            arg_name

        EXAMPLES:
            awu._validate_permitted_values(family, familyPermittedValues)
            If the variable name family has to be retrieved rather than value of the variable, then call
            arg_name = self._deparse_arg_name(arg)

        NOTE:
            This function works only for the the calling function's calling function i.e two frames higher the
            calling function.

            If awu._validate_permitted_values(family, familyPermittedValues) is tha calling function and
            retrieve_name is called in _validate_permitted_values(arg) as arg_name = self._deparse_arg_name(arg) ,
            then name "family" will be retrieved .

        """
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
        for var_name, var_val in callers_local_vars :
            if var_val is var:
                return var_name

        return None

    def _validate_input_columns_not_empty(self, arg, arg_name):
        """
        Function to check whether argument is empty string or not.
        PARAMETERS:
            arg - Argument value (string) to be checked whether it is empty or
                  not.
        RAISES:
            Error if argument contains empty string

        EXAMPLES:
            awu._validate_input_columns_not_empty(arg)
        """
        if isinstance(arg, str):
            if (len(arg.strip()) == 0):
                raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, arg_name),
                                MessageCodes.ARG_EMPTY)

        if isinstance(arg, list):
            for col in arg:
                if (not (col is None) and ((len(col.strip()) == 0))):
                    raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, arg_name),
                                              MessageCodes.ARG_EMPTY)

        return True

    def _validate_permitted_values(self, arg, permitted_values_list, arg_name):
        """
        Function to check the permitted values for the argument.UNSUPPORTED_DATATYPE

        PARAMETERS:
            arg - Argument value (string) to be checked against permitted values
                  from the list.
            permitted_values_list - A list containing permitted values for the
                                  argument.

        RAISES:
            Error if argument is not present in the list

        EXAMPLES:
            permitted_values_list = ["LOGISTIC", "BINOMIAL", "POISSON", "GAUSSIAN", "GAMMA", "INVERSE_GAUSSIAN", "NEGATIVE_BINOMIAL"]
            arg = "LOGISTIC"
            awu._validate_permitted_values(arg, permitted_values_list)
        """
        # validating permitted_values_list type which has to be a list
        if not isinstance(permitted_values_list, list):
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, arg_name, "list"),
                            MessageCodes.UNSUPPORTED_DATATYPE)

        # Validate whether argument has value from permitted values list or not.
        if (not (arg is None) and (arg.upper() not in permitted_values_list)):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INVALID_ARG_VALUE, arg, arg_name, permitted_values_list),
                MessageCodes.INVALID_ARG_VALUE)

        return True

    def _validate_argument_types(self, arg_list):
        """
        Method to verify that the input arguments are of valid data type except for
        argument of DataFrameType.

        PARAMETERS:
           arg_list - A list
                       The argument is expected to be a list of arguments
                       argInfoMatrix = []
                       argInfoMatrix.append(["data", data, False, DataFrame])
                       argInfoMatrix.append(["centers", centers, True, int])
                       argInfoMatrix.append(["threshold", threshold, True, "float"])

        RAISES:
            Error if arguments are not of valid datatype

        EXAMPLES:
            awu._validate_argument_types(arg_list)
        """
        invalid_arg_names = []
        invalid_arg_types = []

        for args in arg_list:
            if args[3] not in ["DataFrame", "formula"]:
                # Verify datatypes for arguments which are required or the optional arguments are not None
                if ((args[2] == True and args[1] is not None) or (args[2] == False)):
                    '''
                    Verify datatypes for arguments which has multiple values
                    provide in List.
                    For example:
                        In Kmeans, initial_seeds takes multiple values which is of string datatype provided
                        in a list. For such verify if all the values are of mentioned datatype.
                        The list is provided as below for multi value arg:
                        initial_seeds = ['2249_51_408_8_14','2165_51_398_7_14.6','2182_51_404_7_14.6',
                                 '2204_55_372_7.19_14.6','2419_44_222_6.6_14.3','2394_44.3_277_7.3_14.5',
                                 '2326_43.6_301_7.11_14.3','2288_44_325_7_14.4']
                    '''
                    if isinstance(args[1], list):
                        for value in args[1]:
                            # if not valid datatype add invalid_arg to dictionary and break
                            if type(value).__name__ != args[3]:
                                invalid_arg_names.append(args[0])
                                invalid_arg_types.append(args[3])
                                break
                    elif type(args[1]).__name__ != args[3]:
                        invalid_arg_names.append(args[0])
                        invalid_arg_types.append(args[3])
        if len(invalid_arg_names) != 0:
            raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, invalid_arg_names , invalid_arg_types ),
                            MessageCodes.UNSUPPORTED_DATATYPE)

        return True

    def _validate_formula_notation(self, formula, data, arg_name):
        """
        _validate_formula_notation method validates input argument is a formula
        or not and returns instance of formula class which contains variable
        names and it's datatypes .
        PARAMETERS:
            formula - formula passed by the user
            data - dataframe object

        RETURNS:
            An instance of formula class.

        EXAMPLES:
            Say we have a formula like:
                y ~ a + b + c + d
                The formula has two parts LHS and RHS with a left-hand side y,
                and a right-hand side, a + b + c + d
                Sometimes you want a formula that has no left-hand side, and
                you can write that as ~ x1 + x2 or even x1 + x2. The RHS
                contains a list of terms separated by '+' .

            Create an instance of formula class as below:
                formulaObject = Formula(independentVars = formula,colTypes = colDesc)

                Using formulaObject we can get the variable names in the formula and
                it's datatypes.

                formula = "admitted ~ masters + gpa + stats + programming"
                awu._validate_formula_notation(formula, df)
        """
        formula_expression = r"^(\s*\w*\s*[~]\s*)*(\w+\s*[+]?\s*)*\s*\w+\s*$"
        unknown_col = []

        if not isinstance(formula, str):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, arg_name, "str"),
                MessageCodes.UNSUPPORTED_DATATYPE)

        #verify formula is not empty.
        if((formula is None) or (len(formula) == 0) or (len(re.sub(' ', '', formula)) == 0)):
            raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, arg_name),
                            MessageCodes.ARG_EMPTY)

        #validate formula expression format
        if bool(re.match(formula_expression,formula)) is False:
            raise TeradataMlException(Messages.get_message(MessageCodes.FORMULA_INVALID_FORMAT, arg_name),
                            MessageCodes.FORMULA_INVALID_FORMAT)

        #get columns and column datatypes of dataframe
        metaexpr = data._metaexpr

        dependent_var,independent_vars = re.split('~', formula)
        if ((len(dependent_var.strip()) == 0) or (len(re.sub(' ', '', dependent_var)) == 0)):
            raise TeradataMlException(Messages.get_message(MessageCodes.FORMULA_MISSING_DEPENDENT_VARIABLE, arg_name),
                                      MessageCodes.FORMULA_MISSING_DEPENDENT_VARIABLE)
        formula_object = Formula(dependent_vars=dependent_var, independent_vars=independent_vars, metaexpr=metaexpr)


        #check if the columns are present in dataframe
        for col in formula_object._get_all_vars():
            if col not in [c.name for c in metaexpr.c]:
                unknown_col.append(col)
        if unknown_col:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDF_UNKNOWN_COLUMN,unknown_col),
                            MessageCodes.TDF_UNKNOWN_COLUMN)

        return formula_object

    def _get_columns_by_type(self, formula_object, data, dtypes):
        """
        Function to generate and return list of column names which are of a
        specific type.

        PARAMETERS:
            formula_object -  Contains  formula object for the argument passed by the user
                             which is generated by _validateFormulaNotation.
            data - A data frame concerning the formula.
            type -  Type of columns to be needed.

        RETURNS:
            A list of column names.

        EXAMPLES:
            awu._get_columns_by_type(formula_object, df,"all")
            awu._get_columns_by_type(formula_object, df,"categorical")
            awu._get_columns_by_type(formula_object, df,"numerical")
        """

        columns_bytype = []
        data_types = []
        common_util = UtilFuncs()
        formula_cols = formula_object._get_independent_vars()

        if dtypes == "all" :
            data_types = common_util._get_all_datatypes()
            formula_cols = formula_object._get_all_vars()
        elif dtypes == "categorical" :
            data_types = common_util._get_categorical_datatypes()
        elif dtypes == "numerical":
            data_types = common_util._get_numeric_datatypes()

        for column in formula_cols:
            for c in data._metaexpr.c:
                if column == c.name and type(c.type) in data_types:
                        columns_bytype.append(column)
                        break

        return columns_bytype

    def _teradata_on_clause_from_dataframe(self, tdframe, lazy = True):
        """
        Function to retrieve the type of data frame and
        corresponding reference to table/view/query.

        PARAMETERS:
            tdframe - dataframe object
            lazy - Parameter to determine the type SQLMR execution.

        RETURNS:
            A dictionary containing reference to dataframe and reference type.

        EXAMPLES:
            awu._teradata_on_clause_from_dataframe(data)
            awu._teradata_on_clause_from_dataframe(data,True)
        """
        aed_utils = AedUtils()
        table_ref = {}

        if tdframe._table_name is not None:
            table_ref['ref'] = tdframe._table_name
        elif not lazy and not aed_utils._aed_is_node_executed(tdframe._nodeid):
            table_ref['ref'] = DataFrameUtils._execute_node_return_db_object_name(tdframe._nodeid)
        else:
            table_ref['ref'] = aed_utils._aed_get_tablename(tdframe._nodeid)
        table_ref['ref_type'] = SourceType.TABLE

        #TODO: Add support for nested level query as in R.
        return table_ref

    def _validate_input_table_datatype(self, data, arg_name, reference_function_name = None):
        """
        Method to verify that the input table parameters of type DataFrame.

        PARAMETERS:
           data - Input table argument.
           reference_function_name - Reference class for the data.

        RAISES:
            Error if table type is not of DataFrame  or provided reference function.

        EXAMPLES:
            awu._validate_input_table_datatype(data)
        """
        if type(data) is list:
            if reference_function_name is not None:
                self._validate_ref_function(data[1], reference_function_name, arg_name)

            else:
                self._validate_input_table_argument(data,arg_name)

        elif reference_function_name is not None:
            self._validate_ref_function(data, reference_function_name, arg_name)

        else:
            self._validate_input_table_argument(data,arg_name)

        return True

    def _validate_ref_function(self, data, ref_fun, arg_name):
        """
        Function to validate data is of provided reference type.

        PARAMETERS:
           data - Input table argument.
           reference_function_name - Reference class for the data.

        RAISES:
            Error if table type of reference function.
        """
        if not(isinstance(data, tdmldf.dataframe.DataFrame)):
            if not(isinstance(data, tdmldf.dataframe.DataFrame)):
                    if(data is not None and not(isinstance(data, ref_fun))):
                        raise TeradataMlException(
                            Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, arg_name,
                                                 "either 'TeradataML DataFrame' or '" + ref_fun.__name__ + "' object"),
                            MessageCodes.UNSUPPORTED_DATATYPE)
        return True

    def _validate_input_table_argument(self, data, arg_name):
        """
        Function to validate data is dataframe type or not.

        PARAMETERS:
           data - Input table argument.

        RAISES:
            Error if table type is not of DataFrame.
        """
        if(not(data is None) and not(isinstance(data,tdmldf.dataframe.DataFrame))) :
                raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, arg_name, "'TeradataML DataFrame'"),
                                MessageCodes.UNSUPPORTED_DATATYPE)
        return True


    def _validate_missing_required_arguments(self,arg_list):
        """
        Method to check whether the required arguments passed to the function are missing
        or not. Only wrapper's use this function.

        PARAMETERS:
           arg_list - A list
                       The argument is expected to be a list of arguments

        RAISES:
            If any arguments are missing exception raised with missing arguments which are
            required.

        EXAMPLES:
                       An example input matrix will be:
                       arg_info_matrix = []
                       arg_info_matrix.append(["data", data, False, DataFrame])
                       arg_info_matrix.append(["centers", centers, True, int])
                       arg_info_matrix.append(["threshold", threshold, True, "float"])
                       awu = AnalyticsWrapperUtils()
                       awu._validate_missing_required_arguments(arg_info_matrix)

        """
        miss_args = []
        for args in arg_list:
            '''
            Check for missing arguments which are required. If args[2] is false
            the argument is required.
            The following conditions are true :
                1. The argument should not be None and an empty string.
                2. The argument should be an instance of Dataframe and Formula.
            then argument is required which is missing and Raises exception.
            '''
            if args[2] == False and ((args[1] is None) and
                   (not(isinstance(args[1], tdmldf.dataframe.DataFrame)) and
                    not(isinstance(args[1],Formula)))):
                        miss_args.append(args[0])
        if (len(miss_args)>0):
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS,miss_args),
                            MessageCodes.MISSING_ARGS)
        return True


    def _create_data_set_object(self, df_input, source_type = "node", database_name = None, metaexpr = None):
        """
        This function helps to create dataframe object.

        PARAMETERS:
           df_input - Name of the table or query or node id.
           source_type - Type of dataframe object to be created.
           database_name - Database name (For future purpose).
           metaexpr - Parent metadata (Sqlalchemy Table Object).

        RETURNS:
             A dataset object of type dataframe.

        EXAMPLES:
            awu = AnalyticsWrapperUtils()
            awu._create_data_set_object("admissioons_train", "table")
            awu._create_data_set_object("select * from admissions_train", "query")
            awu._create_data_set_object(1234, metaexpr)
        """
        if source_type == "node" and metaexpr is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS, "'metaexpr' to create dataframe from node."),
                                      MessageCodes.MISSING_ARGS)

        if source_type == "query":
            return tdmldf.dataframe.DataFrame.from_query(df_input)
        elif source_type == "table":
            if database_name is not None:
                return tdmldf.dataframe.DataFrame(tdmldf.dataframe.in_schema(database_name, df_input))
            return tdmldf.dataframe.DataFrame.from_table(df_input)
        else:
            return tdmldf.dataframe.DataFrame._from_node(df_input, metaexpr)


    def _retrieve_column_info(self, df_input, parameter = None, columns = None):
        """
        Function helps to return column names and it's types for the dataframe.

        When all parameter's are None, it returns all column names and their types.

        When parameter is given, parameter is used as input columns and it's
        corresponding types are returned.

        When column is given, all column names mentioned in columns are returned
        along with their types.

        PARAMETERS:
            df_input - TeradataML dataframe containing columns mentioned
                        in parameter or columns.
            parameter - A parameter passed from a wrapper script containing
                        a list of column names.
            columns - List of column names, if any specific columns from
                        input dataframe or parameter are to be selected.

        RAISES:
            N/A

        RETURNS:
            Column names and corresponding column types in zipped format.

        EXAMPLES:
            awu = AnalyticsWrapperUtils()
            # Retrieve column information for all columns in 'data' dataframe.
            awu._retrieve_column_info(data)
            # Retrieve column information for all of columns in 'accummulate' from 'data' dataframe.
            awu._retrieve_column_info(data, accummulate)
            # Retrieve column information for subset of columns in 'accummulate' from 'data' dataframe.
            awu._retrieve_column_info(data, accummulate, columns_subset)
        """
        col_names = []
        col_types = []
        if df_input is None:
            return zip(col_names, col_types)

        metaexpr = df_input._metaexpr

        if parameter is None and columns is None:
            # Retrieve all Column names & Types from a dataframe _metaexpr
            col_names = [c.name for c in metaexpr.c]
            col_types = [c.type for c in metaexpr.c]

            return zip(col_names, col_types)

        if parameter is not None and columns is None:
            # Retrieve all Column names & Types from a dataframe _metaexpr
            for c in metaexpr.c:
                if c.name.lower() in [col.lower() for col in parameter]:
                    col_names.append(c.name)
                    col_types.append(c.type)

            return zip(col_names, col_types)

        if parameter is not None and columns is not None:
            # Retrieve all Column names & Types from a dataframe _metaexpr
            for c in metaexpr.c:
                if c.name.lower() in [col.lower() for col in parameter] and c.name.lower() in [col.lower() for col in columns]:
                    col_names.append(c.name)
                    col_types.append(c.type)

            return zip(col_names, col_types)

        if parameter is None and columns is not None:
            # Retrieve all Column names & Types from a dataframe _metaexpr
            for c in metaexpr.c:
                if c.name.lower() in [col.lower() for col in columns]:
                    col_names.append(c.name)
                    col_types.append(c.type)

            return zip(col_names, col_types)

    def _get_json_to_sqlalchemy_mapping(self, key):
        """
            This is an internal function used to return a dictionary of all SQLAlchemy Type Mappings.
            It contains mappings from data type from JSON to SQLAlchemyTypes

            PARAMETERS:
                key - Json data type string for which SQLAlchemy Type is needed

            RETURNS:
                dictionary { json_type : SQLAlchemy Type}

            RAISES:
                N/A

            EXAMPLES:
                _get_all_sqlalchemy_mappings()

            """
        # TODO:: Add this to a new class for DataType Mapping and refactor the code elsewhere.
        json_to_sqlalchemy_types_map = {'integer': INTEGER, 'bigint': BIGINT, 'varchar': VARCHAR,
                                        'double precision': FLOAT, 'boolean': BYTEINT}

        return json_to_sqlalchemy_types_map.get(key.lower())

    def _validate_dataframe_has_argument_columns(self, columns, column_arg, data, data_arg):
        """
        Function to check whether column names in columns are present in given dataframe or not.
        This function is used currently only for Analytics wrappers.

        PARAMETERS:
            columns - Column name (a string) or list of column names.
            column_arg - Name of the argument
            data - TeradataML DataFrame to check against for column existence.
            data_arg - DataFrame argument name in wrapper.

        RAISES:
            TeradataMlException - TDMLDF_COLUMN_NOT_FOUND column(s) does not exist in a dataframe.

        EXAMPLES:
            awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data")
        """
        if columns is None:
            return True

        if data is None and columns is not None:
            raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT, column_arg, data_arg),
                                      MessageCodes.DEPENDENT_ARGUMENT)

        if isinstance(columns, str):
            columns = [columns]

        for col in columns:
            if not DataFrameUtils._dataframe_has_column(data, col):
                raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_WRAPPER_ARG_COLUMN_NOT_FOUND, col, column_arg, data_arg),
                    MessageCodes.TDMLDF_WRAPPER_ARG_COLUMN_NOT_FOUND)
