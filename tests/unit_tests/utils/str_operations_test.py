import pytest 

from utils.str_operations import parse_samples, is_percent





class TestParseSamples:
    @pytest.mark.parametrize('_, input, expected', [
        ('empty str', '', []),
        ('int', '123', [123]),
        ('percent', '10 %', ['10%']),
        ('one value', '34,', [34]),
        ('two values', '34, 23%', [34, '23%']),
        ('three values', '34, 23% , 1034', [34, '23%', 1034]),
    ])
    def test_multiple_inputs(self, _, input:str, expected:list[int | str]):
        assert parse_samples(input) == expected
    
    def test_invalid_int_0(self):
        with pytest.raises(ValueError):
            parse_samples('0')

    def test_invalid_int(self):
        with pytest.raises(ValueError):
            parse_samples('-23')

    def test_invalid_percent(self):
        with pytest.raises(ValueError):
            parse_samples('101%')

    def test_invalid_percent_in_list(self):
        with pytest.raises(ValueError):
            parse_samples('12%, 123   ,   345%')

    def test_invalid_format(self):
        with pytest.raises(ValueError):
            parse_samples('not a valid one')

class TestIsPercent:
    
    @pytest.mark.parametrize('_, input, expected', [
        ('empty str', '', False),
        ('invalid format value', 'j10 %', False),
        ('Valid domain value', '10%', True),
        ('Valid domain value with spaces', ' 10% ', True),
        ('Valid edge lower value', '0.004%', True),
        ('valid edge higher value', '100%', True),
        ('invalid edge higher value', '100.00004%', False),
        ('invalid edge lower value', '0%', False),
        ('invalid domain value negative', '-10%', False),
        ('invalid domain value greater than 100', '180%', False),
    ])
    def test_is_percent(self, _, input:str, expected:bool):
        assert is_percent(input) == expected
