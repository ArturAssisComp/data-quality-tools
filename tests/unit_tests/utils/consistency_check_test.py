import math
from typing import Any
import pytest
from tools.data_consistency_inspector.model.documentation import Constraint
from utils.consistency_check import check_type, check_constraints, is_consistent
from globals.types import ConsistencyCheckType as CCT, ConsistencyCheckConstants as CCConstants, ConsistencyCheckSpecialRules as CCSR
from datetime import date


'''
value: valid or invalid
type: with size,  without size
constraints: empty, 1 rule, 2 rules
size: None, 0, or 3
Result: false, true


'''
class TestIsConsistent:
    def test_none(self):
        assert is_consistent(None, CCT.STR, [], None)
    
    def test_the_same_value_with_valid_invalid_constraints(self):
        value = 'hello'
        assert is_consistent(value, CCT.STR, [], None)
        assert not is_consistent(value, CCT.FLOAT, [], None)
        assert is_consistent(value, CCT.CHAR, [Constraint(rule=lambda x: x in {'hello', 'world'}, name='valid set')], None)
        assert not is_consistent(value, CCT.CHAR, [Constraint(rule=lambda x: x in {'helloo', 'world'}, name='valid set')], None)
        assert not is_consistent(value, CCT.CHAR, [Constraint(rule=lambda x: x in {'hello', 'world'}, name='valid set')], 3)
        assert is_consistent(value, CCT.CHAR, [Constraint(rule=lambda x: x in {'hello', 'world'}, name='valid set')], 5)

class TestCheckConstraints:
    @pytest.mark.parametrize(['_', 'values_expected_results', 'constraints'], [
        ('no constraints', [(True, None), ('', None), (None, None)], []),
        (CCSR.TRUE, [(True, None), ('', None), (None, None)], [Constraint(name=CCSR.TRUE.value, rule=None)]),
        ('even integer greater than 3 and less than or equal to 8', 
         [
             ('', 'is even'), (-10, '3 < x <= 8'), (2, '3 < x <= 8'), (3, 'is even'), (4, None),
             (5, 'is even'), (6, None), (7, 'is even'), (8, None), (20000, '3 < x <= 8')
         ], 
         [
            Constraint(name='is even', rule=lambda x: x%2 == 0),
            Constraint(name='3 < x <= 8', rule=lambda x: x > 3 and x <= 8),
         ]),
        ('non-digit or negative', [(True, 'is digit'), ('', 'is digit'), ('hello', 'is digit'), (-1, 'is digit')], [Constraint(name='is digit', rule=str.isdigit), Constraint(name='is non-negative', rule=lambda x: str(x).isdigit() and int(x) >= 0)]),
        ('string with specific length', [('', 'length is 2'), ('a', 'length is 2'), ('ab', None), ('abc', 'length is 2'), ('hello', 'length is 2')], [Constraint(name='length is 2', rule=lambda x: len(x) == 2)]),
        ('multiple of 7', [('', 'multiple of 7'), (14, None), (15, 'multiple of 7'), (21, None), ('49', 'multiple of 7')], [Constraint(name='multiple of 7', rule=lambda x: isinstance(x, int) and x % 7 == 0)]),
        ('even and prime', [(2, None), (3, 'is even'), (4, 'is prime'), (5, 'is even'), (6, 'is prime'), (7, 'is even')], [
            Constraint(name='is even', rule=lambda x: x % 2 == 0),
            Constraint(name='is prime', rule=lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1)))
         ]),
        ('string number in range', [('1', None), ('5', None), ('11', '1 <= x <= 10'), ('0', '1 <= x <= 10'), ('-5', 'string is digit'), ('ten', 'string is digit')], [
            Constraint(name='string is digit', rule=str.isdigit),
            Constraint(name='1 <= x <= 10', rule=lambda x: 1 <= int(x) <= 10)
         ]),
        ('value in set', [('apple', None), ('banana', None), ('cherry', None), ('durian', 'is in set')], [Constraint(name='is in set', rule=lambda x: x in {'apple', 'banana', 'cherry'})]),
        ('type is integer', [(1, None), (1.0, 'is integer'), ('1', 'is integer'), ([1], 'is integer')], [Constraint(name='is integer', rule=lambda x: isinstance(x, int))]),
        ('starts with a and length 5', [('apple', None), ('alpha', None), ('aleph', None), ('array', None), ('anchor', 'length is 5'), ('app', 'length is 5'), ('banana', 'starts with a')], [
            Constraint(name='starts with a', rule=lambda x: isinstance(x, str) and x.startswith('a')),
            Constraint(name='length is 5', rule=lambda x: isinstance(x, str) and len(x) == 5)
         ]),
    ])
    def test_assert_no_constraint(self, _, values_expected_results:list[tuple[Any, bool]], constraints:list[Constraint]):
        for value, expected_result in values_expected_results:
            assert check_constraints(value, constraints) is expected_result



class TestCheckType:
    @pytest.mark.parametrize(['_', 'data_type', 'valid_values_and_expected_values', 'invalid_values'], [
        # Python types
        ('BOOL', CCT.BOOL, [('true', True), ('FALSE', False)], ['tRue', '']),
        ('BOOLEAN', CCT.BOOLEAN, [('TRUE', True), ('false', False)], ['tRue', '']),
        ('STR', CCT.STR, [('', ''), ('j', 'j'), ('oi', 'oi')], []),
        ('STRING', CCT.STRING, [('', ''), ('j', 'j'), ('oi', 'oi')], []),
        ('INT', CCT.INT, [
            ('0', 0), 
            ('01', 1), 
            ('-05', -5), 
            ('10', 10), 
            ('1002544', 1002544)], 
            ['', 'not a number', '1.0', '1.00000000000001', '3+4']),
        ('INTEGER', CCT.INTEGER, [
            ('0', 0), 
            ('01', 1), 
            ('-05', -5), 
            ('10', 10), 
            ('1002544', 1002544)], 
            ['', 'not a number', '1.0', '1.00000000000001', '3+4']),
        ('DATE', CCT.ISO8601_DATE, [
            ('1994-02-23', date(1994,2,23)),
            ('3994-02-03', date(3994,2,3)),
            ('2023-11-02', date(2023,11,2)),  
            ('2000-01-01', date(2000,1,1)),  
            ('20000101', date(2000,1,1)),  
            ('2023-W44-4', date(2023,11,2)), 
        ],
            ['', '1994-22-03', 'not a date', 'a/b/c', '123/22/12223', '2023-13-01', '2000-02-30']),
        # sql server types
        ('ssBIGINT', CCT.ssBIGINT, [
            ('0', 0), 
            ('01', 1), 
            ('-05', -5), 
            ('10', 10), 
            (CCConstants.ssBIGINT_MAX_STR.value, CCConstants.ssBIGINT_MAX.value), 
            (str(CCConstants.ssBIGINT_MAX.value - 1), CCConstants.ssBIGINT_MAX.value - 1), 
            (CCConstants.ssBIGINT_MIN_STR.value, CCConstants.ssBIGINT_MIN.value), 
            (str(CCConstants.ssBIGINT_MIN.value + 1), CCConstants.ssBIGINT_MIN.value + 1), 
            ], 
            ['', 'not a number', '1.0', '1.00000000000001', '3+4', 
             str(CCConstants.ssBIGINT_MAX.value + 1),
             str(CCConstants.ssBIGINT_MIN.value - 1),
             ]),
    ])
    def test_valid_invalid_cases(self, _, data_type:CCT, valid_values_and_expected_values:list[tuple[str, Any]], invalid_values:list[str]):
        for valid_value, expected_valid_value in valid_values_and_expected_values:
            assert (True, expected_valid_value) == check_type(data_type, valid_value, None)
        for invalid_value in invalid_values:
            assert (False, None) == check_type(data_type, invalid_value, None)
    
    @pytest.mark.parametrize(['_', 'data_type', 'valid_values_and_expected_values', 'invalid_values'], [
        # Python types
        ('FLOAT', CCT.FLOAT, [
            ('0.0', 0.0), 
            ('1.0', 1.0), 
            ('-1e3', -1000),
            ('-1.23456', -1.23456),
            ('15', 15.0),
            ], 
            ['', 'oi']),
    ])
    def test_valid_invalid_cases_is_close(self, _, data_type:CCT, valid_values_and_expected_values:list[tuple[str, Any]], invalid_values:list[str]):
        for valid_value, expected_valid_value in valid_values_and_expected_values:
            is_correct_type, current_valid_value = check_type(data_type, valid_value, None)
            assert is_correct_type
            assert math.isclose(expected_valid_value, current_valid_value)
        for invalid_value in invalid_values:
            assert (False, None) == check_type(data_type, invalid_value, None)

    @pytest.mark.parametrize(['_', 'data_type', 'valid_values_and_expected_values_and_size', 'invalid_values_and_size'], [
        # Python types
        ('CHAR', CCT.CHAR, [('', '', 1), ('j', 'j', 1), ('oi', 'oi', 2), ('ola', 'ola', 48), ('abcde', 'abcde', None)], [('12', 1), ('ola', 2)]),
    ])
    def test_valid_invalid_cases_with_sized_types(self, _, data_type:CCT, valid_values_and_expected_values_and_size:list[tuple[str, Any, int]], invalid_values_and_size:list[tuple[str, int]]):
        for valid_value, expected_valid_value, type_size in valid_values_and_expected_values_and_size:
            assert (True, expected_valid_value) == check_type(data_type, valid_value, type_size)
        for invalid_value, type_size in invalid_values_and_size:
            assert (False, None) == check_type(data_type, invalid_value, type_size)