from itertools import combinations_with_replacement
import logging

from tools.data_consistency_inspector.snapshot.dci_base_snapshot import DciBaseSnapshot

from globals.types import get_snapshot_name, SnapshotType, SnapshotMode
from logger.utils import get_custom_logger_name
from tools.data_consistency_inspector.model.documentation import Documentation
import pandas as pd
from utils.dict_operations import init_column_pair
from utils.file_operations import FileOperations
from utils.consistency_check import is_consistent 

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class ColumnPairInconsistencyPatternSnapshot(DciBaseSnapshot):
    _name:str = get_snapshot_name(SnapshotType.COLUMN_PAIR_INCONSISTENCY_PATTERN_SNAPSHOT)
    _type:SnapshotType = SnapshotType.COLUMN_PAIR_INCONSISTENCY_PATTERN_SNAPSHOT
    def __init__(self, documentation:Documentation, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(documentation, logger=logger, fileOperations=fileOperations)




    def perform_specific_processing(self, df:pd.DataFrame, content:dict[str, dict[str, int]], state:SnapshotMode, documentation:Documentation):
        if state == SnapshotMode.SUBSET_MODE:
            df = self._get_subset_columns(df, self._model.columns)

        
        if not df.empty:
            inconsistency_df = self._calculate_inconsistencies(df, documentation)
            

            for col1, col2 in combinations_with_replacement(inconsistency_df.columns, 2):
                num_of_common_inconsistencies = int((inconsistency_df[[col1, col2]].sum(axis=1) == 2).sum())
                if num_of_common_inconsistencies > 0:
                    init_column_pair(col1, col2, content)
                    content[col1][col2] += num_of_common_inconsistencies
                    if col1 != col2:
                        content[col2][col1] += num_of_common_inconsistencies

    def _calculate_inconsistencies(self, df:pd.DataFrame, documentation:Documentation):
            assert documentation.columns
            inconsistency_df = pd.DataFrame()
            for column in documentation.columns:
                new_col_elements = []
                col = column.name
                data_type = column.data_type
                constraints = column.constraints
                type_size = column.type_size
                current_col = df[col]
                for el in current_col:
                    new_col_elements.append(not is_consistent(el, data_type, constraints, type_size))
                inconsistency_df[col] = new_col_elements
            return inconsistency_df

