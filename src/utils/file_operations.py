
import logging
import json
import os

from logger.utils import get_custom_logger_name
import pandas as pd


logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 1, 'last'))


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
