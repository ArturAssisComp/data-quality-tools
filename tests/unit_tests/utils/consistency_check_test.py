import math
from typing import Any
import pytest
from utils.consistency_check import check_type
from globals.types import ConsistencyCheckType as CCT, ConsistencyCheckConstants as CCConstants
from datetime import date





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