import logging
import pytest
from unittest.mock import Mock
import pandas as pd
import numpy as np
from globals.types import SnapshotMode

from tools.data_consistency_inspector.snapshot.row_inconsistency_distribution.row_inconsistency_distribution_snapshot import RowInconsistencyDistributionSnapshot
from utils.file_operations import FileOperations
from tools.data_consistency_inspector.model.documentation import Documentation




class TestRowInconsistencyDistributionSnapshot:
    strict_mode = Documentation(**{
            'columns':[
                    {
                        'name':'A', 
                        'data_type':'str', 
                        'constraints':[
                            {'name':'first letter uppercase', 'rule':'x[0].isupper()'}, 
                            {'name':'last letter lowercase', 'rule':'x[-1].islower()'},
                        ]
                    },
                    {
                        'name':'B', 
                        'data_type':'float', 
                        'constraints':[
                            {'name':'> 0.3', 'rule':'x > 0.3'},
                        ]
                    }
            ], 
            'is_subset_mode':False
        })
    subset_mode = Documentation(**{
            'columns':[
                    {
                        'name':'A', 
                        'data_type':'str', 
                        'constraints':[
                            {'name':'first letter uppercase', 'rule':'x[0].isupper()'}, 
                            {'name':'last letter lowercase', 'rule':'x[-1].islower()'},
                        ]
                    },
                    {
                        'name':'C', 
                        'data_type':'float', 
                        'constraints':[
                            {'name':'> 0.3', 'rule':'x > 0.3'},
                        ]
                    }
            ], 
            'is_subset_mode':True
        })
    df_dict_empty = dict()
    df_dict_only_zero = {'A':[None, 'Ia', 'ValidOne'], 'B':[0.30001, 45, 12.5]}
    df_dict_one_inconsistency = {'A':[None, 'Ia', 'iValidOne'], 'B':[0.30001, 45, 12.5]}
    df_dict_two_inconsistencies= {'A':[None, 'Ia', 'iValidOne'], 'B':[0.30001, 45, .3]}
    initial_content_empty = dict()
    initial_content_some_initial_values = {0:1, 1:1}
    '''
        Documentation	df_dict	initial_content
    1	strict_mode	empty	empty
    2	strict_mode	only_zero	some_initial_values
    3	strict_mode	1 inconsistency	empty
    4	strict_mode	2 inconsistencies	some_initial_values
    5	subset_mode	only_zero	empty
    6	subset_mode	1 inconsistency	some_initial_values
    7	subset_mode	2 inconsistencies	empty
    8	subset_mode	empty	some_initial_values
    '''
    @pytest.mark.parametrize('_, documentation, df_dict, initial_content, final_content', [
        ('1	strict_mode	empty	empty', strict_mode, df_dict_empty, initial_content_empty, dict()),
        ('2	strict_mode	only_zero	some_initial_values', strict_mode, df_dict_only_zero, initial_content_some_initial_values, {0:4, 1:1}),
        ('3	strict_mode	1 inconsistency	empty', strict_mode, df_dict_one_inconsistency, initial_content_empty, {0:2, 1:1}),
        ('4	strict_mode	2 inconsistencies	some_initial_values', strict_mode, df_dict_two_inconsistencies, initial_content_some_initial_values, {0:3, 1:1, 2:1}),
        ('5	subset_mode	only_zero	empty', subset_mode, df_dict_only_zero, initial_content_empty, {0:3}),
        ('6	subset_mode	1 inconsistency	some_initial_values', subset_mode, df_dict_one_inconsistency, initial_content_some_initial_values, {0:3, 1:2}),
        ('7	subset_mode	2 inconsistencies	empty', subset_mode, df_dict_two_inconsistencies, initial_content_empty, {0:2, 1:1}),
        ('8	subset_mode	empty	some_initial_values', subset_mode, df_dict_empty, initial_content_some_initial_values, {0:1, 1:1}),
    ])
    def test_process_dataframe(self, _, documentation:Documentation, df_dict:dict, initial_content:dict, final_content:dict):
        mock_logger = Mock(spec=logging.Logger)
        mock_file_operations = Mock(spec=FileOperations)
        content = initial_content.copy()
        snapshotBuilder = RowInconsistencyDistributionSnapshot(documentation, logger=mock_logger, fileOperations=mock_file_operations)
        df = pd.DataFrame(df_dict)
        state:SnapshotMode
        if documentation.is_subset_mode:
            state = SnapshotMode.SUBSET_MODE
        else:
            state = SnapshotMode.STRICT_MODE

        snapshotBuilder.perform_specific_processing(df, content, documentation=documentation, state=state)
        assert  content == final_content
