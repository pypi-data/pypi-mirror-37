from functools import wraps
from sqlalchemy import func, literal
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import expression


from .sql import _SQLColumnExpression
from .sql_interfaces import ColumnExpression

from teradatasqlalchemy.dialect import preparer, dialect as td_dialect
from teradatasqlalchemy import (CHAR, VARCHAR, CLOB)

# TODO: refactor this once more functions are created
#def _implementation(fn):
#
#  """
#    This decorator wraps sql functions that generate expressions
#    that can be used in DataFrame and Series methods such as assign.
#
#    The wrapper performs error checks as well as implements
#    the kind of ColumnExpression instance to return
#
#    Parameters
#    ----------
#      A function or method that generates sql.
#      The function is from the sql_functions module.
#
#    Examples
#    --------
#      @implementation
#      def unicode_to_latin(x)
#
#  """
#  @wraps
#  def inner(*args, **kw):
#
#      res = fn(*args, **kw)
#      return _SQLColumnExpression(res)
#
#
#@_implementation

def translate(x, source = 'UNICODE', target = 'LATIN'):
  """
  Returns a TRANSLATE(x USING source_TO_target) expression

  Parameters:
  ----------
    x: A ColumnExpression instance coming from the DataFrame
       or output of other functions in sql_functions. A python
       string literal may also be used.

    source, target: str with values:
      - 'UNICODE'
      - 'LATIN'

  References:
  ----------
   Chapter 28: String Operators and Functions
   Teradata® Database SQL Functions, Operators, Expressions, and
   Predicates, Release 16.20

  Examples:
  ----------
    from teradataml.dataframe.sql_functions import translate

    df = DataFrame('df')
    tvshow = df['tvshow']

    res = df.assign(tvshow = translate(tvshow))
  """

  # error checking
  supported = ('UNICODE', 'LATIN')
  if (source not in supported) and (target not in supported):
    raise ValueError('source and target must be in %s' % supported)

  if not isinstance(x, str) and not isinstance(x, ColumnExpression):
    raise ValueError('Only DataFrame columns or python strings are allowed.')

  # get the sqlalchemy expression
  expr = None
  if isinstance(x, ColumnExpression):
    expr = x.expression

  else:
    expr = literal(x, type_ = VARCHAR(length = len(x), charset = 'UNICODE'))

  if not isinstance(expr.type, (CHAR, VARCHAR, CLOB)):
    raise ValueError('Input column must be a character like column.')

  # get the result type
  length, charset = expr.type.length, target
  typ_ = CLOB(length, charset) if isinstance(expr.type, CLOB) else VARCHAR(length, charset)

  # define an inner class to generate the sql expression
  class _translate(expression.FunctionElement):
      name = '_translate'
      type = typ_

  custom = source + '_TO_' + target
  @compiles(_translate)
  def default__translate(element, compiler, **kw):
      column_expression = compiler.process(element.clauses, **kw)
      return ('TRANSLATE({x} USING ' + custom + ')').format(x = column_expression)

  return _SQLColumnExpression(_translate(x.expression))
