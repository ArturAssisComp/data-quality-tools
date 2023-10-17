import logging

from pydantic import BaseModel

from utils.file_operations import FileOperations
from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import tools.null_value_inspector.snapshot.types as types
import pandas as pd
import os




logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))




class BaseSnapshot:
    _logger:logging.Logger
    _file_operations:FileOperations
    _snapshot_model:BaseModel
    _state:types.State
    _documentation:Documentation
    _snapshot_name:str
    _snapshot_filename:str

    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        self._logger = logger
        self._file_operations = fileOperations
        self._state = 'initial'
        self._init_snapshot_name()
        self._snapshot_filename = ''.join([self._snapshot_name, '.json'])
    
    def get_filename(self):
        return self._snapshot_filename
    
    def _init_snapshot_name(self):
        raise NotImplementedError('choose the name from constants files folders names')

    def _set_state(self):
        if self._documentation.is_subset_mode:
            self._state = 'subset-mode'
            if self._documentation.column is None:
                self._logger.error('Invalid documentation for subset-mode: columns expected')
                raise RuntimeError("Invalid documentation")
            self._set_num_of_columns(len(self._documentation.column))
        elif self._documentation.column is None:
            self._state = 'free-mode'
            self._logger.warning('Executing in FREE MODE')
        else:
            self._state = 'strict-mode'
            self._logger.info('Executing in STRICT MODE')
            self._set_num_of_columns(len(self._documentation.column))
        self._snapshot_model.state = self._state
    
    def _set_num_of_columns(self, num_of_columns:int):
        # create a base model for snapshot model
        self._snapshot_model.num_of_columns = num_of_columns
    

    def _reset_snapshot_model(self):
        ''' Executed before creating the snapshot '''
        raise NotImplementedError('Implement this method')


    def create_snapshot(self, dataset: list[str], snapshot_path: str, documentation:Documentation):
        self._documentation = documentation
        self._reset_snapshot_model()
        self._set_state()
        self._logger.info(f'Creating {self._snapshot_name}')
        self._file_operations.loop_through_dataset(dataset, self.process_dataframe)
        self._save_snapshot_to_json(snapshot_path)

    def _save_snapshot_to_json(self, snapshot_path:str):
        # specify the output file path
        output_file = os.path.join(snapshot_path, self._snapshot_filename)

        try:
            self._file_operations.to_json(output_file, self._snapshot_model.model_dump())
            self._logger.info(f'\'{os.path.basename(output_file)}\' created!')
        except Exception as e:
            self._logger.error(f'Error while creating snapshot json: {e}')
            raise

    def _file_will_be_processed(self, documentation:Documentation, state:types.State, df:pd.DataFrame):
        match state:
            case 'initial':
                logger.error('Inconsistent state. Should be free-mode or strict-mode')
                raise RuntimeError
            case 'strict-mode':
                return self._file_will_be_processed_strict_mode(documentation, df)
        return True
    
    def _file_will_be_processed_strict_mode(self, documentation:Documentation, df:pd.DataFrame):
        ''' Check if the file will be processed if the state is strict-mode '''
        file_will_be_processed:bool = True
        if documentation.column:
            columns = set(documentation.column)
            df_columns = set(df.columns)
            if columns != df_columns:
                file_will_be_processed = False
                self._log_difference_column_set(df_columns, columns)
        else:
            logger.error('Inconsistent documentation')
            raise RuntimeError
        return file_will_be_processed
    
    def _log_difference_column_set(self, c1:set, c2:set):
        more = c1 -c2 
        less = c2 - c1 

        more_str = f"+ {more}" if more else ""
        less_str = f"- {less}" if less else ""

        if more_str or less_str:
            logger.warning(f'Invalid columns: {more_str} {less_str}')


    def process_dataframe(self, file_path: str, df: pd.DataFrame, snapshot:BaseModel|None=None, documentation:Documentation|None=None, state:types.State|None=None):
        """
        Process a dataframe to extract snapshot data.

        ## Parameters
        - filename: The name of the source file.
        - df: The dataframe to be processed.
        - snapshot_path: Path to save the snapshot.
        """
        documentation = documentation or self._documentation
        state = state or self._state
        snapshot = snapshot or self._snapshot_model

        if self._file_will_be_processed(documentation, state, df):
            try:
                self._perform_specific_processing(file_path, df, snapshot, state, documentation)
                logger.info(f'OK! ✔️ ')

            except Exception as e:
                self._logger.error(f'Error while processing the file ({file_path}): {e}')
        else:
            logger.warning(f'SKIPPED! X')

    def _perform_specific_processing(self, file_path:str, df:pd.DataFrame, snapshot:BaseModel, state:types.State, documentation:Documentation):
        raise NotImplementedError('specific processing')


        

