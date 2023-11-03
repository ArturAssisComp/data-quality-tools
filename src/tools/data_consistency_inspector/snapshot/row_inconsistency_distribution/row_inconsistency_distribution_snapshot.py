import logging

from tools.data_consistency_inspector.snapshot.dci_base_snapshot import DciBaseSnapshot

from globals.types import get_snapshot_name, SnapshotType, SnapshotMode
from logger.utils import get_custom_logger_name
from tools.data_consistency_inspector.model.documentation import Documentation
import pandas as pd
from utils.file_operations import FileOperations
from utils.consistency_check import is_consistent 

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class RowInconsistencyDistributionSnapshot(DciBaseSnapshot):
    _name:str = get_snapshot_name(SnapshotType.ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT)
    _type:SnapshotType = SnapshotType.ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT
    def __init__(self, documentation:Documentation, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(documentation, logger=logger, fileOperations=fileOperations)




    def perform_specific_processing(self, df:pd.DataFrame, content:dict[int, int], state:SnapshotMode, documentation:Documentation):
        if state == SnapshotMode.SUBSET_MODE:
            df = self._get_subset_columns(df, self._model.columns)
        assert documentation.columns

        
        for _, row in df.iterrows():
            total_inconsistencies = 0
            for column in documentation.columns:
                col = column.name
                type_ = column.type
                constraints = column.constraints
                if not is_consistent(row[col], type_, constraints):
                    total_inconsistencies += 1
            content[total_inconsistencies] = content.get(total_inconsistencies, 0) + 1



