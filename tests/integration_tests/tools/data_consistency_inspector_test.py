import os
import shutil
import json
import pytest
from globals.constants import CONSTANTS
from globals.types import SnapshotType, get_snapshot_name


def clean_folder(base_dir:str):
    shutil.rmtree(os.path.join(base_dir, CONSTANTS.FilesFoldersNames.results))
    shutil.rmtree(os.path.join(base_dir, CONSTANTS.FilesFoldersNames.snapshot))
    os.remove(os.path.join(base_dir, CONSTANTS.FilesFoldersNames.log_filename))

def load_snapshots(base_dir:str):
    row_inconsistency_distribution_snapshot = _load_snapshot(base_dir, get_snapshot_name(SnapshotType.ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT))
    column_inconsistency_count_by_type_snapshot = _load_snapshot(base_dir, get_snapshot_name(SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT))
    return row_inconsistency_distribution_snapshot, column_inconsistency_count_by_type_snapshot

def _load_snapshot(base_dir:str, snapshot_name:str):
    with open(os.path.join(base_dir, f'{CONSTANTS.FilesFoldersNames.snapshot}/{snapshot_name}.json'), 'r') as f:
        snapshot = json.load(f)
    del snapshot['files']
    return snapshot

def execute_command(base_dir:str, midArguments = ''):
        os.chdir(base_dir)
        os.system(f'..\\..\\..\\venv\\Scripts\\data-quality-tools.exe {midArguments} dci')
        return load_snapshots(base_dir)


class TestDataConsistencyInspector:
    @pytest.mark.run(order=1)
    def test_strict_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        row_inconsistency_distribution_snapshot, column_inconsistency_count_by_type_snapshot = execute_command(base_dir, '--doc ./documentation_dci.txt')
        assert row_inconsistency_distribution_snapshot == {
            "type": "row_inconsistency_distribution_snapshot", 
            "population":{"content": {"1": 2}}, 
            "samples":None,
            "state": "strict-mode", 
            "columns":['A', 'B'] 
        }
        assert column_inconsistency_count_by_type_snapshot == {
            "type": "column_inconsistency_count_by_type_snapshot", 
            "population":{"content": {"A": {'even':1}, "B": {'##NOT-NULL##':1}}}, 
            "samples":None,
            "state": "strict-mode", 
            "columns":['A', 'B']
        }
        clean_folder(base_dir)

    @pytest.mark.run(order=2)
    def test_subset_mode(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        row_inconsistency_distribution_snapshot, column_inconsistency_count_by_type_snapshot= execute_command(base_dir, '--doc ./documentation_dci_subset_mode.txt')
        assert row_inconsistency_distribution_snapshot == {
            "type": "row_inconsistency_distribution_snapshot", 
            "population":{"content": {'0':6, "1": 9, '2':4}}, 
            "samples":None,
            "state": "subset-mode", 
            "columns":['A', 'C'] 
        }
        assert column_inconsistency_count_by_type_snapshot == {
            "type": "column_inconsistency_count_by_type_snapshot", 
            "population":{"content": {"A": {'type':3, 'even':7}, "C": {'type':2,'##NOT-NULL##':5}}}, 
            "samples":None,
            "state": "subset-mode", 
            "columns":['A', 'C']
        }
        clean_folder(base_dir)