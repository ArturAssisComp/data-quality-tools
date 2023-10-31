import logging

from globals.types import SnapshotMode, SnapshotType
from tools.base_snapshot.base_snapshot import BaseSnapshot

from globals.types import get_snapshot_name, SnapshotType
from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import pandas as pd
from utils.file_operations import FileOperations 

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class RowNullDistributionSnapshot(BaseSnapshot):
    _name:str = get_snapshot_name(SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT)
    _type:SnapshotType = SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(logger=logger, fileOperations=fileOperations)




    def perform_specific_processing(self, df:pd.DataFrame, content:dict[int, int], state:SnapshotMode, documentation:Documentation):
        if state == SnapshotMode.SUBSET_MODE:
            df = self._get_subset_columns(df, documentation.column)

        for num_of_nulls in df.isnull().sum(axis=1):
            content[num_of_nulls] = content.get(num_of_nulls, 0) + 1
        

