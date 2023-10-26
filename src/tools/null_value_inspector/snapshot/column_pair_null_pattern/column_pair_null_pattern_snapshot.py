import logging

import numpy as np
from globals.types import SnapshotType, get_snapshot_name
from tools.null_value_inspector.snapshot.base_snapshot import BaseSnapshot

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import tools.null_value_inspector.snapshot.types as types
import pandas as pd
from utils.file_operations import FileOperations 

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class ColumnPairNullPatternSnapshot(BaseSnapshot):
    _type:SnapshotType = SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT
    _name:str = get_snapshot_name(SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT)
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(logger=logger, fileOperations=fileOperations)



    def perform_specific_processing(self, df:pd.DataFrame, content:dict[str, dict[str, int]], state:types.State, documentation:Documentation):
        if state == 'subset-mode':
            if documentation.column:
                # TODO refactor: extract function (this code is used in 3 methods)
                missing_columns = set(documentation.column) - set(df.columns)
                if missing_columns:
                    df = df.assign(**{col:np.nan for col in missing_columns})
                df = df[documentation.column]
            else:
                raise RuntimeError('Invalid documentation: expected columns when in subset-mode')

        # TODO refactor
        if len(df) > 0:
            for n, col1 in enumerate(df.columns):
                for i in range(n, len(df.columns)):
                    col2 = df.columns[i]
                    num_of_common_nulls = int((df[[col1, col2]].isna().sum(axis=1) == 2).sum())
                    if num_of_common_nulls > 0:
                        self._init_column_pair(col1, col2, content)
                        content[col1][col2] += num_of_common_nulls
                        if col1 != col2:
                            content[col2][col1] += num_of_common_nulls




    def _init_column_pair(self, col1:str, col2:str, dct:dict):
        if col1 not in dct:
            dct[col1] = {col2:0}
        if col2 not in dct:
            dct[col2] = {col1:0}

        if col1 not in dct[col2]:
            dct[col2][col1] = 0
        if col2 not in dct[col1]:
            dct[col1][col2] = 0

