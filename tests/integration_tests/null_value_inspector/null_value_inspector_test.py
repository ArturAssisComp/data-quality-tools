import os
import shutil
import json
import pytest
from globals.constants import CONSTANTS


def clean_folder(base_dir:str):
    shutil.rmtree(os.path.join(base_dir, CONSTANTS.FilesFoldersNames.results))
    shutil.rmtree(os.path.join(base_dir, CONSTANTS.FilesFoldersNames.snapshot))
    os.remove(os.path.join(base_dir, CONSTANTS.FilesFoldersNames.log_filename))

def load_snapshots(base_dir:str):
    row_null_distribution_snapshot = _load_snapshot(base_dir, CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot)
    column_null_count_snapshot = _load_snapshot(base_dir, CONSTANTS.FilesFoldersNames.column_null_count_snapshot)
    column_pair_null_pattern_snapshot = _load_snapshot(base_dir, CONSTANTS.FilesFoldersNames.column_pair_null_pattern_snapshot)
    return row_null_distribution_snapshot, column_null_count_snapshot, column_pair_null_pattern_snapshot

def _load_snapshot(base_dir:str, snapshot_name:str):
    with open(os.path.join(base_dir, f'{CONSTANTS.FilesFoldersNames.snapshot}/{snapshot_name}.json'), 'r') as f:
        snapshot = json.load(f)
    del snapshot['files']
    return snapshot

def execute_command(base_dir:str, midArguments = ''):
        os.chdir(base_dir)
        os.system(f'dqt {midArguments} nvi -n0 -n1 -n2 -n3')
        return load_snapshots(base_dir)


class TestNullValueInspector:
    @pytest.mark.run(order=1)
    def test_free_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        row_null_distribution_snapshot, column_null_count_snapshot, column_pair_null_pattern_snapshot = execute_command(base_dir)
        assert row_null_distribution_snapshot == {
            "type": "row_null_distribution_snapshot", 
            "content": {"0": 10, "1": 6, "2":1, "3": 1, "4": 1}, 
            "state": "free-mode", 
            "columns":[]
        }
        assert column_null_count_snapshot == {
            "type": "column_null_count_snapshot", 
            "state": "free-mode", 
            "content": {"A": 3, "B": 8, "C": 3, "D": 1},
            "columns":[]
        }
        assert column_pair_null_pattern_snapshot == {
            'type': 'column_pair_null_pattern_snapshot',
            'content':{
                'A':{'A':3, 'B':2, 'C':2, 'D':1}, 
                'B':{'A':2, 'B':8, 'C':3, 'D':1}, 
                'C':{'A':2, 'B':3, 'C':3, 'D':1}, 
                'D':{'A':1, 'B':1, 'C':1, 'D':1}
            },
            'state':'free-mode',
            "columns":[]
        }

        clean_folder(base_dir)

    @pytest.mark.run(order=2)
    def test_strict_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        row_null_distribution_snapshot, column_null_count_snapshot, column_pair_null_pattern_snapshot = execute_command(base_dir, '--doc ./documentation.txt')
        assert row_null_distribution_snapshot == {
            "type": "row_null_distribution_snapshot", 
            "content": {"0": 1, "1": 1}, 
            "state": "strict-mode", 
            "columns":['A', 'B']
        }
        assert column_null_count_snapshot == {
            "type": "column_null_count_snapshot", 
            "state": "strict-mode", 
            "content": {"A": 0, "B": 1}, 
            "columns":['A', 'B']

        }
        assert column_pair_null_pattern_snapshot == {
            'type': 'column_pair_null_pattern_snapshot',
            'content':{'B':{'B':1}},
            'state':'strict-mode', 
            "columns":['A', 'B']

        }
        clean_folder(base_dir)

    @pytest.mark.run(order=3)
    def test_subset_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        row_null_distribution_snapshot, column_null_count_snapshot, column_pair_null_pattern_snapshot = execute_command(base_dir, '--doc ./documentation_subset_mode.txt')
        assert row_null_distribution_snapshot == {
            "type": "row_null_distribution_snapshot", 
            "content": {"0": 13, "1": 4, "2":2}, 
            "state": "subset-mode", 
            "columns":['A', 'C'] 
        }
        assert column_null_count_snapshot == {
            "type": "column_null_count_snapshot", 
            "state": "subset-mode", 
            "content": {"A": 3, "C": 5}, 
            "columns":['A', 'C']
        }
        assert column_pair_null_pattern_snapshot == {
            'type': 'column_pair_null_pattern_snapshot',
            'content':{
                'A':{'A':3, 'C':2}, 
                'C':{'A':2, 'C':5}, 
            },
            'state':'subset-mode', 
            "columns":['A', 'C']
        }
        clean_folder(base_dir)