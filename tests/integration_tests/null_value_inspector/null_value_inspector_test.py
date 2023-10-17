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
    with open(os.path.join(base_dir, f'{CONSTANTS.FilesFoldersNames.snapshot}/{CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot}.json'), 'r') as f:
        row_null_distribution_snapshot = json.load(f)
    del row_null_distribution_snapshot['files']
    with open(os.path.join(base_dir, f'{CONSTANTS.FilesFoldersNames.snapshot}/{CONSTANTS.FilesFoldersNames.column_null_count_snapshot}.json'), 'r') as f:
        column_null_count_snapshot = json.load(f)
    del column_null_count_snapshot['files']
    return row_null_distribution_snapshot, column_null_count_snapshot

class TestNullValueInspector:
    @pytest.mark.run(order=1)
    def test_free_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(base_dir)
        os.system('dqt  nvi -n0 -n1')
        row_null_distribution_snapshot, column_null_count_snapshot = load_snapshots(base_dir)
        assert row_null_distribution_snapshot == {
            "type": "row_null_distribution_snapshot", 
            "content": {"0": 10, "1": 6, "2":1, "3": 1, "4": 1}, 
            "state": "free-mode", 
            "num_of_columns": None
        }
        assert column_null_count_snapshot == {
            "type": "column_null_count_snapshot", 
            "state": "free-mode", 
            "num_of_columns": 4, 
            "content": {"A": 3, "B": 8, "C": 3, "D": 1}
        }

        clean_folder(base_dir)

    @pytest.mark.run(order=2)
    def test_strict_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(base_dir)
        os.system('dqt --doc ./documentation.txt  nvi -n0 -n1')
        row_null_distribution_snapshot, column_null_count_snapshot = load_snapshots(base_dir)
        assert row_null_distribution_snapshot == {
            "type": "row_null_distribution_snapshot", 
            "content": {"0": 1, "1": 1}, 
            "state": "strict-mode", 
            "num_of_columns": 2 
        }
        assert column_null_count_snapshot == {
            "type": "column_null_count_snapshot", 
            "state": "strict-mode", 
            "num_of_columns": 2, 
            "content": {"A": 0, "B": 1}
        }
        clean_folder(base_dir)

    @pytest.mark.run(order=3)
    def test_subset_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(base_dir)
        os.system('dqt --doc ./documentation_subset_mode.txt  nvi -n0 -n1')
        row_null_distribution_snapshot, column_null_count_snapshot = load_snapshots(base_dir)
        assert row_null_distribution_snapshot == {
            "type": "row_null_distribution_snapshot", 
            "content": {"0": 13, "1": 4, "2":2}, 
            "state": "subset-mode", 
            "num_of_columns": 2 
        }
        assert column_null_count_snapshot == {
            "type": "column_null_count_snapshot", 
            "state": "subset-mode", 
            "num_of_columns": 2, 
            "content": {"A": 3, "C": 5}
        }
        clean_folder(base_dir)