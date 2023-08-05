# -*- coding: utf-8 -*-
"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: ellen.nolan@teradata.com
Secondary Owner:

teradataml.common.constants
----------
A class for holding all constants
"""
import re
from enum import Enum
from teradatasqlalchemy.types import (INTEGER, SMALLINT, BIGINT, BYTEINT, DECIMAL, FLOAT, NUMBER)
from teradatasqlalchemy.types import (DATE, TIME, TIMESTAMP)
from teradatasqlalchemy.types import (BYTE, VARBYTE, BLOB)
from teradatasqlalchemy.types import (CHAR, VARCHAR, CLOB)

class SQLConstants(Enum):
    SQL_BASE_QUERY = 1
    SQL_SAMPLE_QUERY = 2
    SQL_SAMPLE_WITH_WHERE_QUERY = 3
    SQL_CREATE_VOLATILE_TABLE_FROM_QUERY_WITH_DATA = 4
    SQL_CREATE_VOLATILE_TABLE_FROM_QUERY_WITHOUT_DATA = 5
    SQL_CREATE_VOLATILE_TABLE_USING_COLUMNS = 6
    SQL_CREATE_TABLE_FROM_QUERY_WITH_DATA = 7
    SQL_HELP_COLUMNS = 8
    SQL_DROP_TABLE = 9
    SQL_DROP_VIEW = 10
    SQL_NROWS_FROM_QUERY = 11
    SQL_TOP_NROWS_FROM_TABLEORVIEW = 12
    SQL_INSERT_INTO_TABLE_VALUES = 13
    SQL_SELECT_COLUMNNAMES_FROM = 14
    SQL_SELECT_DATABASE = 15
    SQL_HELP_VOLATILE_TABLE = 16
    SQL_SELECT_TABLE_NAME = 17
    SQL_CREATE_VIEW = 18
    SQL_SELECT_USER = 19
    SQL_HELP_VIEW = 20
    SQL_HELP_TABLE = 21
    SQL_HELP_INDEX = 22
    SQL_INSERT_ALL_FROM_TABLE = 23
    SQL_SELECT_DATABASENAME = 24
    SQL_AND_TABLE_KIND = 25
    SQL_AND_TABLE_NAME = 26
    SQL_AND_TABLE_NAME_LIKE = 27

class TeradataConstants(Enum):
    TERADATA_VIEW = 1
    TERADATA_TABLE = 2
    TABLE_COLUMN_LIMIT = 2048
    DEFAULT_VAR_SIZE = 1024
    TERADATA_JOINS = ["inner", "left", "right", "full"]

class AEDConstants(Enum):
    AED_NODE_NOT_EXECUTED = 0
    AED_NODE_EXECUTED     = 1
    AED_DB_OBJECT_NAME_BUFFER_SIZE = 128
    AED_NODE_TYPE_BUFFER_SIZE = 32
    AED_ASSIGN_DROP_EXISITING_COLUMNS = "Y"
    AED_ASSIGN_DO_NOT_DROP_EXISITING_COLUMNS = "N"
    AED_QUERY_NODE_TYPE_ML_QUERY_SINGLE_OUTPUT = "ml_query_single_output"
    AED_QUERY_NODE_TYPE_ML_QUERY_MULTI_OUTPUT = "ml_query_multi_output"
    AED_QUERY_NODE_TYPE_REFERENCE = "reference"

class SourceType:
    TABLE = "TABLE"
    QUERY = "QUERY"

class PythonTypes:
    PY_NULL_TYPE = "nulltype"
    PY_INT_TYPE = "int"
    PY_FLOAT_TYPE = "float"
    PY_STRING_TYPE = "str"
    PY_DECIMAL_TYPE = "decimal.Decimal"
    PY_DATETIME_TYPE = "datetime.datetime"
    PY_TIME_TYPE = "datetime.time"
    PY_DATE_TYPE = "datetime.date"
    PY_BYTES_TYPE = "bytes"

class TeradataTypes:
    TD_INTEGER_TYPES = [INTEGER, BYTEINT, SMALLINT, BIGINT]
    TD_INTEGER_CODES = ["I", "I1", "I2", "I8"]
    TD_FLOAT_TYPES = [FLOAT]
    TD_FLOAT_CODES = ["F"]
    TD_DECIMAL_TYPES = [DECIMAL, NUMBER]
    TD_DECIMAL_CODES = ["D", "N"]
    TD_BYTE_TYPES = [BYTE, VARBYTE, BLOB]
    TD_BYTE_CODES = ["BF", "BV", "BO"]
    TD_DATETIME_TYPES = [TIMESTAMP]
    TD_DATETIME_CODES = ["TS", "SZ"]
    TD_TIME_TYPES = [TIME]
    TD_TIME_CODES = ["AT", "TZ"]
    TD_DATE_TYPES = [DATE]
    TD_DATE_CODES = ["DA"]
    TD_NULL_TYPE = "NULLTYPE"

class TeradataTableKindConstants:
    VOLATILE = "volatile"
    TABLE = "table"
    VIEW = "view"
    TEMP = "temp"
    ALL  = "all"
    ML_PATTERN = "ml_%"
    VOLATILE_TABLE_NAME = 'Table Name'
    REGULAR_TABLE_NAME = 'TableName'

class SQLPattern:
    SQLMR = re.compile(r"SELECT \* FROM .*\((\s*.*)*\) as .*", re.IGNORECASE)
    DRIVER_FUNC_SQLMR = re.compile(".*OUT\s+TABLE.*", re.IGNORECASE)
    SQLMR_REFERENCE_NODE = re.compile("reference:.*:.*", re.IGNORECASE)
