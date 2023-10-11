import math
from utils.statistics import std_dev_weighted
import pytest


class TestStdDevWeighted:
    def test_negative_key(self):
        weighted_dict = {0:12, 3:2, 6:6, -2:9, 2:3}
        with pytest.raises(ValueError):
            std_dev_weighted(weighted_dict)

    def test_negative_value(self):
        weighted_dict = {0:12, 3:2, 6:-6, 2:9, 2:3}
        with pytest.raises(ValueError):
            std_dev_weighted(weighted_dict)

    def test_zero_items(self):
        weighted_dict = {0:0, 3:0}
        with pytest.raises(ValueError):
            std_dev_weighted(weighted_dict)

    def test_empty_dict(self):
        weighted_dict = dict()
        with pytest.raises(ValueError):
            std_dev_weighted(weighted_dict)
    
    @pytest.mark.parametrize('_, distribution, expectedValue', [
        ['one item', {0:1}, 0],
        ['3 equal items', {28:3}, 0],
        ['2 different values', {0:1, 1:1}, 0.5],
        ['11 values', {0:1, 1:3, 3:4, 45:3}, 19.23194656],
    ])
    def test_valid_values(self, _, distribution:dict[int, int], expectedValue:float):
        assert math.isclose(std_dev_weighted(distribution), expectedValue)