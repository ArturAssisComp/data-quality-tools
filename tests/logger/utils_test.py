import pytest
from logger.utils import get_custom_logger_name

class TestGetCustomLoggerName:
    @pytest.mark.parametrize('_, args, expectedFirst, expectedLast', [
        ('empty name', [''], '', ''),
        ('1 name', ['name'], '', ''),
        ('2 names with space', ['name1. name2'], 'name1', ' name2'),
        ('3 names', ['name1.name2.name3'], 'name1.name2', 'name2.name3'),
        ('empty name, with len_minus_depth = 2', ['', 2], '', ''),
        ('1 name, with len_minus_depth = 2', ['name', 2], '', ''),
        ('2 names, with len_minus_depth = 2', ['name1.name2', 2], '', ''),
        ('3 names, with len_minus_depth = 2', ['name1.name2.name3', 2], 'name1', 'name3'),
    ])
    def test_valid_cases(self, _, args:list, expectedFirst:str, expectedLast):
        assert get_custom_logger_name(*args) == expectedFirst
        assert get_custom_logger_name(*args, start='last') == expectedLast

