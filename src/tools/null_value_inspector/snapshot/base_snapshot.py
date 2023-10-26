import logging
import time
from typing import Callable

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
            self._model.columns = self._documentation.column.copy()
        elif self._documentation.column is None:
            self._state = 'free-mode'
            self._logger.warning('Executing in FREE MODE')
        else:
            self._state = 'strict-mode'
            self._logger.info('Executing in STRICT MODE')
            self._model.columns = self._documentation.column.copy()
        self._model.state = self._state
    
    


    
    def _init_snapshot_model(self):
        ''' Initialize the snapshot model that will be used '''
        self._model = SnapshotModel(type=self._type)


    def create_snapshot(self, dataset: list[str], snapshot_path: str, documentation:Documentation, samples:list[str|int] | None):
        self._documentation = documentation
        self._init_snapshot_model()
        self._set_state()
        self._logger.info(f'Creating {self._name}')
        # loop through the dataset returning csv files that are valid
        for csv_file in self._file_operations.dataset_csv_generator(dataset):
            if csv_file:
                self.process_csv_file(csv_file, samples)
        self._save_snapshot_to_json(snapshot_path)

    def _save_snapshot_to_json(self, snapshot_path:str):
        # specify the output file path
        output_file = os.path.join(snapshot_path, self._filename)

        try:
            self._file_operations.to_json(output_file, self._model.model_dump())
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
                    if snapshot.samples is None:
                        snapshot.samples = dict()
                    # process samples
                    for sample in samples:
                        key = str(sample)
                        snapshot.samples[key] = {'content':dict()}
                        sample_str = f'(sample - {key})'
                        value, is_int = get_int_or_float(sample)
                        if is_int:
                            # get value rows from csv file
                            self._process_dataframe_in_chunks(file_path, CSV_CHUNK_SIZE, snapshot.samples[key]['content'], snapshot.files, state, documentation, self._file_operations.csv_generator_abs_sample, sample_str=sample_str, **{'sample_abs_size':value})
                        else:
                            # get value % rows from the csv file
                            rel_value = value/100
                            self._process_dataframe_in_chunks(file_path, CSV_CHUNK_SIZE, snapshot.samples[key]['content'], snapshot.files, state, documentation, self._file_operations.csv_generator_rel_sample,  sample_str=sample_str, **{'sample_rel_size':rel_value})
                else:
                    # process population
                    if snapshot.population is None:
                        snapshot.population = {'content':dict()}
                    self._process_dataframe_in_chunks(file_path, CSV_CHUNK_SIZE, snapshot.population['content'], snapshot.files, state, documentation, self._file_operations.csv_generator)
            except Exception as e:
                self._logger.error(f'Error while processing the file ({file_path}): {e}')
        else:
            self._logger.warning(f'SKIPPED! X')

    def _process_dataframe_in_chunks(self, target_file_path:str, chunksize:int, content:dict, files:list, state:types.State, documentation:Documentation, generator_func:Callable, sample_str:str='', **kwargs):
        initial_time = time.time()
        for df in generator_func(target_file_path, chunksize=chunksize, dtype=str, **kwargs):
            self.perform_specific_processing(df, content, state, documentation)
        files.append(target_file_path)
        final_time = time.time()
        self._logger.info(f'OK! ✔️   ({final_time - initial_time:.2f} s) ({sample_str})')


    def perform_specific_processing(self, df:pd.DataFrame, content:dict, state:types.State, documentation:Documentation):
        raise NotImplementedError('specific processing')
        

