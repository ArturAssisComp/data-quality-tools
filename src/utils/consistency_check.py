
from datetime import date
import numpy as np
from typing import Any, Literal
from tools.data_consistency_inspector.model.documentation import Constraint
from globals.types import ConsystencyCheckType as CCT


SPECIAL_RULES = Literal['##not-null##']


# TODO refactor
def is_consistent(value, data_type:CCT, constraints:list[Constraint]):
    if value in {np.nan, None}:
        for constraint in constraints:
            if constraint.name == '##not-null##':
                return False
            
        return True
    # check the type
    value = str(value)
    has_correct_type, final_value = check_type(data_type, value)
    if not has_correct_type:
        return False
    
    # check the constraints
    # TODO extract check constraints
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
def check_type(data_type:CCT, value:str)->tuple[bool, Any]:
    '''
    TODO 
    ## Exact numerics
    - [ ] bigint
    - [ ] numeric
    - [ ] bit
    - [ ] smallint
    - [ ] decimal
    - [ ] smallmoney
    - [ ] int
    - [ ] tinyint
    - [ ] money
    '''
    final_value:Any = None
    has_correct_type:bool = False
    match data_type:
        case CCT.STR | CCT.STRING:
            has_correct_type, final_value = True, value
        case CCT.INT | CCT.INTEGER:
            has_correct_type, final_value = _check_int(value)
        case CCT.FLOAT:
            has_correct_type, final_value = _check_float(value)
        case CCT.BOOL | CCT.BOOLEAN:
            has_correct_type, final_value = _check_boolean(value)
        case CCT.ISO8601_DATE:
            has_correct_type, final_value = _check_iso8601date(value)
        #Sql Server types
        # Exact numerics
        # not implemented yet
        case _:
            raise NotImplementedError(f'Type not implemented yet: {data_type}')
    return has_correct_type, final_value


def _check_int(value:str)->tuple[bool, Any]:
    try:
        final_value = int(value)
        has_correct_type = True
    except:
        final_value = None
        has_correct_type = False
    return has_correct_type, final_value


def _check_float(value:str)->tuple[bool, Any]:
    try:
        final_value = float(value)
        has_correct_type = True
    except:
        final_value = None
        has_correct_type = False
    return has_correct_type, final_value

def _check_boolean(value:str)->tuple[bool, Any]:
    if value in {'true', 'True', 'TRUE'}:
        final_value = True
        has_correct_type = True
    elif value in {'false', 'False', 'FALSE'}:
        final_value = False
        has_correct_type = True
    else:
        final_value = None
        has_correct_type = False
    return has_correct_type, final_value

def _check_iso8601date(value:str)->tuple[bool, Any]:
    try:
        final_value = date.fromisoformat(value)
        has_correct_type = True
    except:
        final_value = None
        has_correct_type = False
    return has_correct_type, final_value