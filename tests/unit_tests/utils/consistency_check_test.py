from typing import Any
import pytest
from utils.consistency_check import check_type
from globals.types import ConsystencyCheckType as CCT





class TestCheckType:

    @pytest.mark.parametrize(['_', 'data_type', 'valid_values_and_expected_values', 'invalid_values'], [
        # Python types
        ('BOOL', CCT.BOOL, [('true', True), ('FALSE', False)], ['tRue', '']),
        ('BOOLEAN', CCT.BOOLEAN, [('TRUE', True), ('false', False)], ['tRue', '']),
    ])
    def test_valid_invalid_cases(self, _, data_type:CCT, valid_values_and_expected_values:list[tuple[str, Any]], invalid_values:list[str]):
        for valid_value, expected_valid_value in valid_values_and_expected_values:
            assert (True, expected_valid_value) == check_type(data_type, valid_value)
        for invalid_value in invalid_values:
            assert (False, None) == check_type(data_type, invalid_value)