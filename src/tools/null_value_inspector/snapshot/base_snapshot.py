import logging
import time

from tools.null_value_inspector.snapshot.base_model import BaseSnapshotModel
from tools.null_value_inspector.snapshot.model.snapshot_model import  SnapshotModel

from globals.types import SnapshotType 
from utils.file_operations import FileOperations
from utils.str_operations import get_int_or_float
from logger.utils import get_custom_logger_name
from tools.null_value_inspector.model.documentation import Documentation
import tools.null_value_inspector.snapshot.types as types
import pandas as pd
import os




logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))




class BaseSnapshot:
    _logger:logging.Logger
    _file_operations:FileOperations
    # TODO current_refactoring: _snapshot_model2 will replace _snapshot_model when this session is over
    _snapshot_model:BaseSnapshotModel
    _model:SnapshotModel 
    _state:types.State
    _documentation:Documentation
    _name:str
    _type:SnapshotType
    _filename:str

    def __init__(self, logger:logging.Logger = logger, fileOperations:FileOperations = FileOperations()):
        self._logger = logger
        self._file_operations = fileOperations
        self._state = 'initial'
        self._filename = ''.join([self._name, '.json'])
    
    def get_filename(self):
        return self._filename
    

    def _set_state(self):
        if self._documentation.is_subset_mode:
            self._state = 'subset-mode'
            if self._documentation.column is None:
                self._logger.error('Invalid documentation for subset-mode: columns expected')
                raise RuntimeError("Invalid documentation")
            self._snapshot_model.columns = self._documentation.column.copy() # TODO current_refactoring: remove this line
            self._model.columns = self._documentation.column.copy()
        elif self._documentation.column is None:
            self._state = 'free-mode'
            self._logger.warning('Executing in FREE MODE')
        else:
            self._state = 'strict-mode'
            self._logger.info('Executing in STRICT MODE')
            self._snapshot_model.columns = self._documentation.column.copy() # TODO current_refactoring: remove this line
            self._model.columns = self._documentation.column.copy()
        self._snapshot_model.state = self._state # TODO current_refactoring: remove this line
        self._model.state = self._state
    
    

    # TODO current_refactoring: _reset_snapshot_model will be replaced by _init_snapshot_model
    def _reset_snapshot_model(self):
        ''' Executed before creating the snapshot '''
        raise NotImplementedError('Implement this method')

    
    def _init_snapshot_model(self):
        ''' Initialize the snapshot model that will be used '''
        self._model = SnapshotModel(type=self._type)


    def create_snapshot(self, dataset: list[str], snapshot_path: str, documentation:Documentation, samples:list[str|int] | None):
        self._documentation = documentation
        self._reset_snapshot_model() # TODO current_refactoring: remove this later
        self._init_snapshot_model()
        self._set_state()
        self._logger.info(f'Creating {self._name}')
        self._file_operations.loop_through_dataset(dataset, self.process_dataframe) # eliminate in the future
        # loop through the dataset returning csv files that are valid
        for csv_file in self._file_operations.dataset_csv_generator(dataset):
            if csv_file:
                self.process_csv_file(csv_file, samples)
        self._save_snapshot_to_json(snapshot_path)
        self._save_snapshot_to_json2(snapshot_path)

    def _save_snapshot_to_json2(self, snapshot_path:str):
        # specify the output file path
        output_file = os.path.join(snapshot_path, self._filename + 'sample')

        try:
            self._file_operations.to_json(output_file, self._model.model_dump())
            self._logger.info(f'\'{os.path.basename(output_file)}\' created!')
        except Exception as e:
            self._logger.error(f'Error while creating snapshot json: {e}')
            raise
    def _save_snapshot_to_json(self, snapshot_path:str):
        # specify the output file path
        output_file = os.path.join(snapshot_path, self._filename)

        try:
            self._file_operations.to_json(output_file, self._snapshot_model.model_dump())
            self._logger.info(f'\'{os.path.basename(output_file)}\' created!')
        except Exception as e:
            self._logger.error(f'Error while creating snapshot json: {e}')
            raise

    def _file_will_be_processed(self, documentation:Documentation, state:types.State, df:pd.DataFrame):
        match state:
            case 'initial':
                self._logger.error('Inconsistent state. Should be free-mode or strict-mode')
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
            self._logger.error('Inconsistent documentation')
            raise RuntimeError
        return file_will_be_processed
    
    def _log_difference_column_set(self, c1:set, c2:set):
        more = c1 -c2 
        less = c2 - c1 

        more_str = f"+ {more}" if more else ""
        less_str = f"- {less}" if less else ""

        if more_str or less_str:
            self._logger.warning(f'Invalid columns: {more_str} {less_str}')

    def process_csv_file(self, file_path: str, samples:list[int|str]|None, snapshot:SnapshotModel|None=None, documentation:Documentation|None=None, state:types.State|None=None):
        """
        Process a csv file to extract snapshot data.

        ## Parameters
        - file_path: the path to the csv source path.
        - samples: if None, it will use all the data. If provided, it will use only <number> rows or <percentage> from the population, 
        selected randomly.
        """
        documentation = documentation or self._documentation
        state = state or self._state
        snapshot = snapshot or self._model
        CSV_CHUNK_SIZE = 250000

        sample_df = pd.read_csv(file_path, nrows=10)
        if self._file_will_be_processed(documentation, state, sample_df):
            try:
                if samples:
                    # process samples
                    for sample in samples:
                        value, is_int = get_int_or_float(sample)
                        if is_int:
                            # get value rows from csv file
                            pass
                        else:
                            # get value % rows from the csv file
                            pass
                else:
                    # process population
                    if snapshot.population is None:
                        snapshot.population = {'content':dict()}
                    initial_time = time.time()
                    for df in pd.read_csv(file_path, chunksize=CSV_CHUNK_SIZE, dtype=str):
                        self._perform_specific_processing2(df, snapshot.population['content'], state, documentation)
                    snapshot.files.append(file_path)
                    final_time = time.time()
                    self._logger.info(f'OK! ✔️   ({final_time - initial_time:.2f} s)')
            except Exception as e:
                self._logger.error(f'Error while processing the file ({file_path}): {e}')
        else:
            self._logger.warning(f'SKIPPED! X')


    def process_dataframe(self, file_path: str, df: pd.DataFrame, snapshot:BaseSnapshotModel|None=None, documentation:Documentation|None=None, state:types.State|None=None):
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
                initial_time = time.time()
                self._perform_specific_processing(df, snapshot, state, documentation)
                snapshot.files.append(file_path)
                final_time = time.time()
                self._logger.info(f'OK! ✔️   ({final_time - initial_time:.2f} s)')

            except Exception as e:
                self._logger.error(f'Error while processing the file ({file_path}): {e}')
        else:
            self._logger.warning(f'SKIPPED! X')

    def _perform_specific_processing(self, df:pd.DataFrame, snapshot:BaseSnapshotModel, state:types.State, documentation:Documentation):
        raise NotImplementedError('specific processing')


    def _perform_specific_processing2(self, df:pd.DataFrame, content:dict, state:types.State, documentation:Documentation):
        raise NotImplementedError('specific processing')
        

