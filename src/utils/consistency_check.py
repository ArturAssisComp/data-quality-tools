
import numpy as np
from typing import Literal
from tools.data_consistency_inspector.model.documentation import Constraint


SPECIAL_RULES = Literal['##not-null##']


def is_consistent(value:str, type_:str, constraints:list[Constraint]):
    if value in {np.nan, None}:
        for constraint in constraints:
            if constraint.name == '##not-null##':
                return False
            
        return True
    # check the type
    match type_:
        case 'str':
            final_value = value
        case 'int':
            try:
                final_value = int(value)
            except:
                return False
        case 'float':
            try:
                final_value = float(value)
            except:
                return False
        case 'bool':
            if value in {'true', 'True', 'TRUE'}:
                final_value = True
            elif value in {'false', 'False', 'FALSE'}:
                final_value = False
            else:
                return False
        case _:
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

