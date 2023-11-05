import logging
from tools.base_snapshot.base_snapshot import BaseSnapshot

from tools.base_snapshot.model.snapshot_model import SnapshotModel

from globals.types import SnapshotMode 
from utils.file_operations import FileOperations
from logger.utils import get_custom_logger_name
from tools.data_consistency_inspector.model.documentation import Documentation
import pandas as pd




logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))





class DciBaseSnapshot(BaseSnapshot):
    _documentation:Documentation
    def __init__(self, documentation:Documentation, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        super().__init__(documentation, logger=logger, fileOperations=fileOperations)

    def _set_state(self):
        if self._documentation.is_subset_mode:
            self._state = SnapshotMode.SUBSET_MODE
            if self._documentation.columns is None:
                self._logger.error('Invalid documentation for subset-mode: columns expected')
                raise RuntimeError("Invalid documentation")
        elif self._documentation.columns is None:
            self._logger.error('Invalid documentation for strict-mode: columns expected')
            raise RuntimeError("Invalid documentation")
        else:
            self._state = SnapshotMode.STRICT_MODE
            self._logger.info('Executing in STRICT MODE')
        self._model.state = self._state
        self._model = SnapshotModel(**self._model.model_dump()) # this is necessary to revalidate the enum field
        self._get_columns()
    
    def _get_columns(self):
        if self._documentation.columns:
            self._model.columns = list(map(lambda x:x.name, self._documentation.columns.copy())) 
        else:
            self._model.columns = []
    


    
    def _file_will_be_processed_strict_mode(self, documentation:Documentation, df:pd.DataFrame):
        ''' Check if the file will be processed if the state is strict-mode '''
        file_will_be_processed:bool = True
        if documentation.columns:
            columns = set(self._model.columns)
            df_columns = set(df.columns)
            if columns != df_columns:
                file_will_be_processed = False
                self._log_difference_column_set(df_columns, columns)
        else:
            self._logger.error('Inconsistent documentation')
            raise RuntimeError
        return file_will_be_processed

