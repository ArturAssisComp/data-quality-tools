import logging
import pytest
from unittest.mock import Mock
import pandas as pd
import numpy as np
import copy

from tools.null_value_inspector.snapshot.column_pair_null_pattern.column_pair_null_pattern_snapshot import ColumnPairNullPatternSnapshot
from utils.file_operations import FileOperations
import tools.null_value_inspector.snapshot.column_pair_null_pattern.model.model as model 
from tools.null_value_inspector.model.documentation import Documentation
import tools.null_value_inspector.snapshot.types as types 



class TestColumnPairNullPatternSnapshot:
    free_mode = Documentation()
    strict_mode = Documentation(column=["A", 'B'])
    subset_mode = Documentation(column=['A', 'C'], is_subset_mode=True)
    df_dict_empty = dict()
    df_dict_only_zero = {'A':[12], 'B':['hi']}
    df_dict_one_zero_one_nonzero = {'A':[2, np.nan, 34], 'B':[5, np.nan, np.nan]} 
    initial_content_empty = dict()
    initial_content_one_with_zero = {'A':{'B':0}, 'B':{'A':0}}
    initial_content_one_zero_one_nonzero = {'A':{'B':12, 'C':0}, 'B':{'A':12, 'C':0}, 'C':{'A':0, 'B':0}}



    '''
    Pairwise test cases:
    	documentation	df_dict	initial_content
    1	free-mode	one_zero	one_zero
    2	free-mode	one_zero_one_nonzero	one_zero_one_non_zero
    3	strict-mode	one_zero	one_zero_one_non_zero
    4	strict-mode	one_zero_one_nonzero	empty
    5	strict-mode	no element	empty
    6	strict-mode	no element	one_zero
    7	subset-mode	one_zero_one_nonzero	empty
    8	subset-mode	no element	one_zero
    9	subset-mode	no element	one_zero_one_non_zero
    10	subset-mode	one_zero	empty
    11	free-mode	no element	one_zero_one_non_zero
    12	free-mode	one_zero	empty
    13	free-mode	one_zero_one_nonzero	one_zero
    '''
    @pytest.mark.parametrize('_, documentation, df_dict, initial_content, final_content', [
        ('domain test case', Documentation(), {"A":[1, np.nan, 3], "B":[1, np.nan, np.nan], 'C':[2, np.nan, np.nan]}, dict(), {'A':{'B':1, 'C':1}, 'B':{'A':1, 'C':2}, 'C':{'A':1, 'B':2}}),
        ('pairwise 1', free_mode, df_dict_only_zero, initial_content_one_with_zero, {'A':{'B':0}, 'B':{'A':0}}),
        ('pairwise 2', free_mode, df_dict_one_zero_one_nonzero, initial_content_one_zero_one_nonzero, {'A':{'B':13, 'C':0}, 'B':{'A':13, 'C':0}, 'C':{'A':0, 'B':0}}), 
        ('pairwise 3', strict_mode, df_dict_only_zero, initial_content_one_zero_one_nonzero, {'A':{'B':12, 'C':0}, 'B':{'A':12, 'C':0}, 'C':{'A':0, 'B':0}}), 
        ('pairwise 4', strict_mode, df_dict_one_zero_one_nonzero, initial_content_empty, {'A':{'B':1}, 'B':{'A':1}}), 
        ('pairwise 5', strict_mode, df_dict_empty, initial_content_empty, dict()), 
        ('pairwise 6', strict_mode, df_dict_empty, initial_content_one_with_zero, {'A':{'B':0}, 'B':{'A':0}}), 
        ('pairwise 7', subset_mode, df_dict_one_zero_one_nonzero, initial_content_empty, {'A':{'C':1}, 'C':{'A':1}}), 
        ('pairwise 8', subset_mode, df_dict_empty, initial_content_one_with_zero, {'A':{'B':0}, 'B':{'A':0}}), 
        ('pairwise 9', subset_mode, df_dict_empty, initial_content_one_zero_one_nonzero,{'A':{'B':12, 'C':0}, 'B':{'A':12, 'C':0}, 'C':{'A':0, 'B':0}}), 
        ('pairwise 10', subset_mode, df_dict_only_zero ,initial_content_empty,{'A':{'C':0}, 'C':{'A':0}}), 
        ('pairwise 11', free_mode ,df_dict_empty ,initial_content_one_zero_one_nonzero,{'A':{'B':12, 'C':0}, 'B':{'A':12, 'C':0}, 'C':{'A':0, 'B':0}}), 
        ('pairwise 12', free_mode ,df_dict_only_zero ,initial_content_empty,{'A':{'B':0}, 'B':{'A':0}}), 
        ('pairwise 13', free_mode ,df_dict_one_zero_one_nonzero ,initial_content_one_with_zero,{'A':{'B':1}, 'B':{'A':1}}),
    ])
    def test_process_dataframe(self, _, documentation:Documentation, df_dict:dict, initial_content:dict, final_content:dict):
        mock_logger = Mock(spec=logging.Logger)
        mock_file_operations = Mock(spec=FileOperations)
        snapshot = model.ColumnPairNullPatternSnapshotModel.get_basic_instance()
        snapshot.content = copy.deepcopy(initial_content)
        snapshotBuilder = ColumnPairNullPatternSnapshot(logger=mock_logger, fileOperations=mock_file_operations)
        df = pd.DataFrame(df_dict)
        state:types.State
        if documentation.is_subset_mode:
            state = 'subset-mode'
        elif documentation.column:
            state = 'strict-mode'
        else:
            state = 'free-mode'

        snapshotBuilder.process_dataframe('filename', df, snapshot=snapshot, documentation=documentation, state=state)
        assert  snapshot.content == final_content
