import logging

from globals.types import SnapshotMode, SnapshotType, get_snapshot_name
from tools.null_value_inspector.snapshot.nvi_base_snapshot import NviBaseSnapshot

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import pandas as pd
from utils.file_operations import FileOperations 

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class ColumnPairNullPatternSnapshot(NviBaseSnapshot):
    _type:SnapshotType = SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT
    _name:str = get_snapshot_name(SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT)
    def __init__(self, documentation:Documentation, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(documentation, logger=logger, fileOperations=fileOperations)



    def perform_specific_processing(self, df:pd.DataFrame, content:dict[str, dict[str, int]], state:SnapshotMode, documentation:Documentation):
        if state == SnapshotMode.SUBSET_MODE:
            df = self._get_subset_columns(df, documentation.column)
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

