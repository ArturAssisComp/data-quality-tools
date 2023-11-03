
from datetime import date
import re
import numpy as np
from typing import Any, Literal
from tools.data_consistency_inspector.model.documentation import Constraint
from globals.types import ConsistencyCheckType as CCT, ConsistencyCheckConstants as CCConstants, ConsistencyCheckSpecialRules as CCSR


SPECIAL_RULES = Literal['##not-null##']


# TODO refactor
def is_consistent(value, data_type:CCT, constraints:list[Constraint], type_size:int|None):
    if value in {np.nan, None}:
        for constraint in constraints:
            if constraint.name == CCSR.NOT_NULL.value:
                return False
            
        return True
    # check the type
    value = str(value)
    has_correct_type, final_value = check_type(data_type, value, type_size)
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


def check_constraints(final_value, constraints:list[Constraint]):
    for constraint in constraints:
        function_name, args = _extract_function_and_args(constraint.name)
        if function_name:
            function_name = ''.join(['##', function_name, '##'])
            if _handle_special_rules(function_name, args):
                continue
            return False

        else:
            if constraint.rule is None:
                continue
            try:
                if not constraint.rule(final_value):
                    return False
            except:
                return False
    return True


def _handle_special_rules(function_name:str, args:list[str]):
    match function_name:
        case CCSR.FALSE.value:
            return False
        case CCSR.TRUE.value:
            return True
        case _:
            raise ValueError(f'Invalid special rule: {function_name}')

def _extract_function_and_args(s)->tuple[str|None, list[str]]:
    pattern = r"^##(.*?)\((.*?)\)##$"
    match = re.search(pattern, s)
    if match:
        function_name = match.group(1)
        args = match.group(2).split(',')
        return function_name, [arg.strip() for arg in args]
    else:
        return None, [] 

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
def check_type(data_type:CCT, value:str, type_size:int|None)->tuple[bool, Any]:
    '''
    TODO 
    ## Exact numerics
    - [X] bigint
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
        case CCT.CHAR:
            has_correct_type, final_value = _check_char(value, type_size)
        #Sql Server types
        # Exact numerics
        case CCT.ssBIGINT:
            has_correct_type, final_value = _check_ssBigint(value)
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

def _check_char(value:str, type_size:int|None)->tuple[bool, Any]:
    assert type_size is None or (type_size is not None and type_size > 0)
    if type_size is not None and len(value) > type_size:
        final_value = None
        has_correct_type = False
    else:
        final_value = value
        has_correct_type = True
    return has_correct_type, final_value

## sql server types
def _check_ssBigint(value:str)->tuple[bool, Any]:
    try:
        final_value = int(value)
        if final_value < CCConstants.ssBIGINT_MIN.value or final_value > CCConstants.ssBIGINT_MAX.value:
            raise ValueError
        has_correct_type = True
    except:
        final_value = None
        has_correct_type = False
    return has_correct_type, final_value