import logging

from tools.data_consistency_inspector.snapshot.dci_base_snapshot import DciBaseSnapshot

from globals.types import get_snapshot_name, SnapshotType, SnapshotMode
from logger.utils import get_custom_logger_name
from tools.data_consistency_inspector.model.documentation import Documentation
import pandas as pd
from utils.file_operations import FileOperations
from utils.consistency_check import get_inconsistency

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class ColumnInconsistencyCountByTypeSnapshot(DciBaseSnapshot):
    _name:str = get_snapshot_name(SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT)
    _type:SnapshotType = SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT
    def __init__(self, documentation:Documentation, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(documentation, logger=logger, fileOperations=fileOperations)




    def perform_specific_processing(self, df:pd.DataFrame, content:dict[str, dict[str, int]], state:SnapshotMode, documentation:Documentation):
        if state == SnapshotMode.SUBSET_MODE:
            df = self._get_subset_columns(df, self._model.columns)
        assert documentation.columns


        for column in documentation.columns:
            col = column.name
            data_type = column.data_type
            constraints = column.constraints
            type_size = column.type_size
            for value in df[col]:
                inconsistency = get_inconsistency(value, data_type, constraints, type_size)
                if inconsistency is not None:
                    content[col] = content.get(col, dict())
                    content[col][inconsistency] = content[col].get(inconsistency, 0) + 1
        