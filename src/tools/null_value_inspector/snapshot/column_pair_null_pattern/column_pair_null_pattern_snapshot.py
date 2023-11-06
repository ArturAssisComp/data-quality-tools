from itertools import combinations_with_replacement
import logging

from globals.types import SnapshotMode, SnapshotType, get_snapshot_name
from tools.null_value_inspector.snapshot.nvi_base_snapshot import NviBaseSnapshot

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import pandas as pd
from utils.dict_operations import init_column_pair
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

        if not df.empty:
            for col1, col2 in combinations_with_replacement(df.columns, 2):
                num_of_common_nulls = int((df[[col1, col2]].isna().sum(axis=1) == 2).sum())
                if num_of_common_nulls > 0:
                    init_column_pair(col1, col2, content)
                    content[col1][col2] += num_of_common_nulls
                    if col1 != col2:
                        content[col2][col1] += num_of_common_nulls



