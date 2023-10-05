import logging
from globals.constants import CONSTANTS
from typing import Literal

from utils.file_operations import FileOperations
from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import pandas as pd
import os
import tools.null_value_inspector.snapshot.row_null_distribution.model.model as model 




logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

SNAPSHOT_STATE = Literal['initial', 'free-mode', 'strict-mode']


class RowNullDistributionSnapshot:
    _logger:logging.Logger
    _fileOperations:FileOperations
    _row_null_distribution_snapshot:model.RowNullDistributionSnapshot
    _state:SNAPSHOT_STATE
    _documentation:Documentation

    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
        self._state = 'initial'

    def _set_state(self):
        if self._documentation.column is None:
            self._state = 'free-mode'
            self._logger.warning('Executing in FREE MODE')
        else:
            self._state = 'strict-mode'
            self._logger.info('Executing in STRICT MODE')
        self._row_null_distribution_snapshot.state = self._state

    def _reset(self):
        ''' Executed before creating the snapshot '''
        self._row_null_distribution_snapshot = model.RowNullDistributionSnapshot.get_basic_instance()
        self._row_null_distribution_snapshot.content = dict()
        self._set_state()


    def create_row_null_distribution_snapshot(self, dataset: list[str], snapshot_path: str, documentation:Documentation):
        self._documentation = documentation
        self._reset()
        self._logger.info('Creating Row Null Distribution Snapshot')
        df_processing_method = self.process_dataframe_to_row_null_distribution_snapshot
        self._loop_through_dataset(dataset, df_processing_method)
        self._save_snapshot_to_json(snapshot_path)

    def _save_snapshot_to_json(self, snapshot_path:str):
        # specify the output file path
        output_file = os.path.join(snapshot_path, ''.join([CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot, '.json']))

        try:
            self._fileOperations.to_json(output_file, self._row_null_distribution_snapshot.model_dump())
            self._logger.info(f'\'{os.path.basename(output_file)}\' created!')
        except Exception as e:
            self._logger.error(f'Error while creating snapshot json: {e}')
            raise

    def _file_will_be_processed(self, documentation:Documentation, state:SNAPSHOT_STATE, df:pd.DataFrame):
        file_will_be_processed:bool = True
        match state:
            case 'initial':
                logger.error('Inconsistent state. Should be free-mode or strict-mode')
                raise RuntimeError
            case 'strict-mode':
                if documentation.column:
                    columns = set(documentation.column)
                    df_columns = set(df.columns)
                    if columns != df_columns:
                        file_will_be_processed = False
                        more = df_columns - columns
                        less = columns - df_columns

                        more_str = f"+ {more}" if more else ""
                        less_str = f"- {less}" if less else ""

                        if more_str or less_str:
                            logger.warning(f'Invalid columns: {more_str} {less_str}')
                else:
                    logger.error('Inconsistent documentation')
                    raise RuntimeError
        return file_will_be_processed


    def process_dataframe_to_row_null_distribution_snapshot(self, file_path: str, df: pd.DataFrame, documentation:Documentation|None=None, state:SNAPSHOT_STATE|None=None):
        """
        Process a dataframe to extract row null distribution and save it as a snapshot.

        ## Parameters
        - filename: The name of the source file.
        - df: The dataframe to be processed.
        - snapshot_path: Path to save the snapshot.
        """
        if documentation is None:
            documentation = self._documentation
        if state is None:
            state = self._state

        if self._file_will_be_processed(documentation, state, df):
            try:
                self._row_null_distribution_snapshot.files.append(file_path)
                for num_of_nulls in df.isnull().sum(axis=1):
                    self._row_null_distribution_snapshot.content[num_of_nulls] = self._row_null_distribution_snapshot.content.get(num_of_nulls, 0) + 1
                logger.info(f'OK! ✔️ ')

            except Exception as e:
                self._logger.error(f'Error while processing the file ({file_path}): {e}')
        else:
            logger.warning(f'SKIPPED! X')

        
    # TODO extract the following methods in the future for other snapshots

    def _loop_through_dataset(self, dataset:list[str], df_processing_method):
        for file_or_dir in dataset:
            file_or_dir = os.path.abspath(file_or_dir)
            if os.path.isdir(file_or_dir):
                self._process_directory(file_or_dir, df_processing_method)
            else:
                self._process_file(file_or_dir, df_processing_method)
    


    def _process_directory(self, directory: str, df_processing_method):
        self._logger.info(f'Scanning dir: \'{directory}\'')
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(".csv"):
                    full_path = os.path.join(dirpath, filename)
                    self._process_file(full_path, df_processing_method)

    def _process_file(self, full_path:str, df_processing_method):
        self._logger.info(f'Processing file {full_path}')
        df = self._fileOperations.read_csv(full_path)
        df_processing_method(full_path, df)
