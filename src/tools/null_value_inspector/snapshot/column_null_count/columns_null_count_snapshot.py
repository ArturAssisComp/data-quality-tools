import logging

from globals.types import SnapshotMode, SnapshotType, get_snapshot_name
from tools.null_value_inspector.snapshot.base_snapshot import BaseSnapshot

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import pandas as pd
from utils.file_operations import FileOperations 

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class ColumnNullCountSnapshot(BaseSnapshot):
    _type:SnapshotType = SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT
    _name:str = get_snapshot_name(SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT)
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(logger=logger, fileOperations=fileOperations)
        



    def perform_specific_processing(self, df:pd.DataFrame, content:dict[str, int], state:SnapshotMode, documentation:Documentation):
        if state == SnapshotMode.SUBSET_MODE:
            df = self._get_subset_columns(df, documentation.column)
        for col in df.columns:
            content[col] = content.get(col, 0) + int(df[col].isnull().sum())
        

