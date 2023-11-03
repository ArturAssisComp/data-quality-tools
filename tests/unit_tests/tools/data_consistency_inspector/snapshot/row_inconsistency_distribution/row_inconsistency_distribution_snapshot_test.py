import logging
import pytest
from unittest.mock import Mock
import pandas as pd
import numpy as np
from globals.types import SnapshotMode

from tools.data_consistency_inspector.snapshot.row_inconsistency_distribution.row_inconsistency_distribution_snapshot import RowInconsistencyDistributionSnapshot
from utils.file_operations import FileOperations
from tools.data_consistency_inspector.model.documentation import Documentation



class TestRowNullDistributionSnapshot:
    strict_mode = Documentation(**{'columns':[{'name':'A', 'type':'str'}], 'is_subset_mode':'true'})
    #subset_mode = Documentation(columns=['A', 'C'], is_subset_mode=True)
    df_dict_empty = dict()
    df_dict_one_zero = {'A':[12], 'B':['hi']}
    df_dict_one_zero_one_nonzero = {'A':[2, np.nan], 'B':[5, np.nan]}
    initial_content_empty = dict()
    initial_content_one_zero = {0:1}
    initial_content_one_zero_one_nonzero = {0:1, 1:1}



    @pytest.mark.parametrize('_, documentation, df_dict, initial_content, final_content', [
        ('domain test case', strict_mode, {"A":[1, 2, 3], "B":[1, np.nan, np.nan], 'C':[2, 'hi', 3]}, dict(), {0:3}),
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
