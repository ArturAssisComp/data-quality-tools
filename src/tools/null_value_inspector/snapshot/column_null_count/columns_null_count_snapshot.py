import logging

import numpy as np
from globals.types import SnapshotType, get_snapshot_name
from tools.null_value_inspector.snapshot.base_snapshot import BaseSnapshot

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import tools.null_value_inspector.snapshot.types as types
import pandas as pd
import tools.null_value_inspector.snapshot.column_null_count.model.model as model
from utils.file_operations import FileOperations 

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class ColumnNullCountSnapshot(BaseSnapshot):
    _type:SnapshotType = SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT
    _name:str = get_snapshot_name(SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT)
    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(logger=logger, fileOperations=fileOperations)
        
    def _reset_snapshot_model(self):
        ''' Executed before creating the snapshot '''
        self._snapshot_model = model.ColumnNullCountSnapshotModel.get_basic_instance()

    def _perform_specific_processing(self, df:pd.DataFrame, snapshot:model.ColumnNullCountSnapshotModel, state:types.State, documentation:Documentation):
        if state == 'subset-mode':
            if documentation.column:
                missing_columns = set(documentation.column) - set(df.columns)
                if missing_columns:
                    df = df.assign(**{col:np.nan for col in missing_columns})
                df = df[documentation.column]
            else:
                raise RuntimeError('Invalid documentation: expected columns when in subset-mode')
        for col in df.columns:
            snapshot.content[col] = snapshot.content.get(col, 0) + int(df[col].isnull().sum())


        

