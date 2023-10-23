
import logging
import json
import os

from logger.utils import get_custom_logger_name
from enum import Enum
import pandas as pd


logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))

class CsvFileStatus(Enum):
    VALID_CSV = 0
    INVALID_CSV = 1
    NOT_CSV = 2


class FileOperations:
    _logger:logging.Logger
    def __init__(self, logger:logging.Logger = logger):
        self._logger = logger

    def read_csv(self, filename:str):
        try:
            df = pd.read_csv(filename)
            return df
        except Exception as e:
            self._logger.error(f'Invalid CSV file ({filename}): {e}')
            raise
    def read_Json(self, filename:str):
        try:
            with open(filename, 'r') as f:
                js = json.load(f)
                return js
        except Exception as e:
            self._logger.error(f'Invalid JSON file ({filename}): {e}')
            raise

        
    def to_json(self, filename:str, content:dict):
        try:
            with open(filename, 'w') as f:
                json.dump(content, f)
        except Exception as e:
            self._logger.error(f'Cannot save the file \'{filename}\' as json: {e}')
            raise

    def create_directory(self, path:str):
        try:
            if not os.path.isdir(path):
                os.makedirs(path)
        except Exception as e:
            logger.error(f'Not able to create directories for {os.path.basename(path)} path: {e}')
            raise
    
    def dataset_csv_generator(self, dataset:list[str]):
        '''
        Generates valid csv file path while looping through `dataset`. If the csv
        file is not valid, returns None.
        '''
        for file_or_dir in dataset:
            file_or_dir = os.path.abspath(file_or_dir)
            if os.path.isfile(file_or_dir):
                match self._checked_csv_file(file_or_dir):
                    case CsvFileStatus.VALID_CSV:
                        yield file_or_dir
                    case _:
                        yield None
            elif os.path.isdir(file_or_dir):
                for file in self._directory_csv_generator(file_or_dir):
                    yield file
            else:
                self._logger.warning(f"Invalid path: {file_or_dir}. Neither a file nor a directory.")
    
    def loop_through_dataset(self, dataset:list[str], processing_method):
        """
        Iterates through a list of dataset paths, processing each file or directory.

        This method is designed to process a dataset comprising a mix of individual
        files and directories. Directories are recursively searched for `.csv` files
        to process. Each found file or directory is processed using the provided
        `processing_method`.

        Parameters:
        -----------
        dataset : list[str]
            A list containing paths to individual files or directories. Directories
            are recursively searched for `.csv` files.

        processing_method : callable
            The processing method to apply to each file. The method should accept two
            parameters: the file path (str) and the dataframe (DataFrame) read from
            the file.

        Examples:
        ---------
        >>> def sample_processing(file_path, df):
        ...     print(f"Processed {file_path} with {len(df)} rows.")
        ...
        >>> obj.loop_through_dataset(['./data/sample.csv', './data/folder'], sample_processing)

        Notes:
        ------
        - Assumes that all files in the provided directories with the `.csv` extension
        are valid and meant to be processed.
        - The method uses the absolute path for both files and directories.

        """
        for file_or_dir in dataset:
            file_or_dir = os.path.abspath(file_or_dir)
            if os.path.isfile(file_or_dir):
                self._process_file(file_or_dir, processing_method)
            elif os.path.isdir(file_or_dir):
                self._process_directory(file_or_dir, processing_method)
            else:
                self._logger.warning(f"Invalid path: {file_or_dir}. Neither a file nor a directory.")



    def _directory_csv_generator(self, directory:str):
        for dirpath, _, filenames in os.walk(directory):
            self._logger.info(f'Scanning dir: \'{directory}\'')
            for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    match self._checked_csv_file(full_path):
                        case CsvFileStatus.VALID_CSV:
                            yield full_path
                        case CsvFileStatus.INVALID_CSV:
                            yield None

    def _process_directory(self, directory: str, processing_method):
        self._logger.info(f'Scanning dir: \'{directory}\'')
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith((".csv", ".CSV")):
                    full_path = os.path.join(dirpath, filename)
                    self._process_file(full_path, processing_method)

    def _process_file(self, full_path:str, df_processing_method):
        self._logger.info(f'Processing file {full_path}')
        try:
            df = self.read_csv(full_path)
            df_processing_method(full_path, df)
        except:
            self._logger.error('ERROR! X')

    def _checked_csv_file(self, full_path:str)->CsvFileStatus:
        if self._ends_with_csv(full_path):
            self._logger.info(f'Checking file {full_path}')
            try:
                pd.read_csv(full_path, nrows=10)
                return CsvFileStatus.VALID_CSV
            except:
                self._logger.error('Invalid csv file')
                return CsvFileStatus.INVALID_CSV
        return CsvFileStatus.NOT_CSV

    def _ends_with_csv(self, full_path:str):
        return full_path.endswith((".csv", ".CSV"))