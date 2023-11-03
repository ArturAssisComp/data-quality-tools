import math
from typing import Any
import pytest
from utils.consistency_check import check_type
from globals.types import ConsystencyCheckType as CCT





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
    ])
    def test_valid_invalid_cases(self, _, data_type:CCT, valid_values_and_expected_values:list[tuple[str, Any]], invalid_values:list[str]):
        for valid_value, expected_valid_value in valid_values_and_expected_values:
            assert (True, expected_valid_value) == check_type(data_type, valid_value)
        for invalid_value in invalid_values:
            assert (False, None) == check_type(data_type, invalid_value)
    
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
            is_correct_type, current_valid_value = check_type(data_type, valid_value)
            assert is_correct_type
            assert math.isclose(expected_valid_value, current_valid_value)
        for invalid_value in invalid_values:
            assert (False, None) == check_type(data_type, invalid_value)
