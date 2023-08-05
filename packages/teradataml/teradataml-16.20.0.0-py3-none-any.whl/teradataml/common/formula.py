"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: mounika.kotha@teradata.com
Secondary Owner:
    
This file implements processing of formula variables that will be used 
in Teradata Vantage Analytical function wrappers.
"""

import re 

class Formula(object):
    """
    This class contains all the variables and datatypes of the formula input provided
    by the user.
    """
    def __init__(self, metaexpr, independent_vars, dependent_vars=None):
        """
        Constructor for the Formula class.
        PARAMETERS:
            metaexpr - Parent meta data (_MetaExpression object).
            dependent_vars - Variable on the LHS of the formula.
            independent_vars - Variables on the RHS of the formula.
        
        EXAMPLE:
            Formula = "admitted ~ masters + gpa + stats + programming"
            dependent_vars - admitted
            independent_vars - masters + gpa + stats + programming
         RETURNS:
            A formula object.
        """
        self.dependent_vars = dependent_vars
        self.independent_vars = independent_vars
        self.metaexpr = metaexpr
        
    def _get_all_vars(self):
        """
        Method returns a list which contains all the variables of the formula.
        """
        all_vars = self._get_independent_vars()
        if self.dependent_vars is not None:
            all_vars.insert(0,self._get_dependent_vars())
        return all_vars
    
    def _get_dependent_vars(self):
        """
        Method returns variable on the LHS of the formula.
        """
        return self.dependent_vars.strip()
    
    def _get_independent_vars(self):
        """
        Method returns variable on the RHS of the formula.
        """
        return self._var_split(self.independent_vars)
    
    def _var_split(self, var):
        """
        Split string into multiple strings when a delimiters 
        ('~', '+', '-', '*', '/', ':', '**') occurs.
        PARAMETERS:
            string  - var to split
        RETURNS:
            A List .
        """
        split_expr = re.split(r"[~+/*:-]?[**]?\s*", var)
        varlist = filter(None,split_expr)
        return list(varlist)