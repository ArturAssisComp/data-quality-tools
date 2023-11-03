
import numpy as np
from typing import Any, Literal
from tools.data_consistency_inspector.model.documentation import Constraint


SPECIAL_RULES = Literal['##not-null##']


# TODO refactor
def is_consistent(value, type_:str, constraints:list[Constraint]):
    if value in {np.nan, None}:
        for constraint in constraints:
            if constraint.name == '##not-null##':
                return False
            
        return True
    # check the type
    value = str(value)
    has_correct_type, final_value = _check_type(type_, value)
    if not has_correct_type:
        return False
    
    # check the constraints
    for constraint in constraints:
        if constraint.rule is None:
            continue
        try:
            if not constraint.rule(final_value):
                return False
        except:
            return False
    return True

# TODO implement other data types using sql server as base:
'''
Data types:
https://learn.microsoft.com/en-us/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver16

https://learn.microsoft.com/en-us/sql/t-sql/data-types/date-and-time-types?view=sql-server-ver16
date (Transact-SQL)
datetime (Transact-SQL)
datetime2 (Transact-SQL)
datetimeoffset (Transact-SQL)
smalldatetime (Transact-SQL)
time (Transact-SQL)

https://learn.microsoft.com/en-us/sql/t-sql/data-types/numeric-types?view=sql-server-ver16
bit (Transact-SQL)
decimal and numeric (Transact-SQL)
float and real (Transact-SQL)
int, bigint, smallint, and tinyint (Transact-SQL)
money and smallmoney (Transact-SQL)

https://learn.microsoft.com/en-us/sql/t-sql/data-types/string-and-binary-types?view=sql-server-ver16
binary & varbinary
char & varchar
nchar & nvarchar
ntext, text, & image

'''
def _check_type(type_:str, value:str):
    final_value:Any = None
    has_correct_type:bool = False
    match type_:
        case 'str' | 'STR' | 'STRING' | 'string':
            final_value = value
            has_correct_type = True
        case 'int' | 'INT' | 'integer' | 'INTEGER':
            try:
                final_value = int(value)
                has_correct_type = True
            except:
                final_value = None
                has_correct_type = False
        case 'float' | 'FLOAT':
            try:
                final_value = float(value)
                has_correct_type = True
            except:
                final_value = None
                has_correct_type = False
        case 'bool' | 'BOOL' | 'boolean' | 'BOOLEAN':
            if value in {'true', 'True', 'TRUE'}:
                final_value = True
                has_correct_type = True
            elif value in {'false', 'False', 'FALSE'}:
                final_value = False
                has_correct_type = True
            else:
                final_value = None
                has_correct_type = False
        case _:
            final_value = None
            has_correct_type = False
    return has_correct_type, final_value
