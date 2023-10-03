from globals.interfaces import BaseToolClass
from globals.constants import CONSTANTS
from tools.null_value_inspector.model.tool_arguments import ToolArguments
from tools.null_value_inspector.model.documentation import Documentation
from logger.utils import log_footer, log_header
import pandas as pd
import os
import logging
import json

logger = logging.getLogger(__name__)

TAB = '  '


class NullValueInspector(BaseToolClass):
    _tmp_snapshot_id:int

    def _get_documentation(self, documentation_path:str):
        try:
            with open(documentation_path, 'r') as f:
                # Load JSON data from file
                data = json.load(f)
                documentation = Documentation(**data)
        except Exception as e:
            logger.info(f'No documentation provided: {e}')
            documentation = Documentation(**dict())
        return documentation
    
    def _create_snapshot_directory(self, snapshot_path:str):
        try:
            if not os.path.isdir(snapshot_path):
                os.makedirs(snapshot_path)
        except Exception as e:
            logger.error(f'Not able to create directories for snapshot path: {e}')
            raise


    def _create_snapshots(self, tool_arguments:ToolArguments, snapshot_path:str, documentation:Documentation):
        if tool_arguments.null_distribution_by_row_overview:

            log_header(logger, 'Initializing Snapshots')
            self._create_snapshot_directory(snapshot_path)
            self._create_row_null_distribution_snapshot(tool_arguments.dataset, snapshot_path, documentation)
            log_footer(logger, 'Snapshots Finished    ')

    
    def _create_results(self, tool_arguments:ToolArguments):
        log_header(logger, 'Initializing Results')
        if tool_arguments.null_distribution_by_row_overview:
            logger.info('Creating null-distribution-by-row-overview')

        log_footer(logger, 'Results Finished    ')


    def work_on(self, tool_arguments: ToolArguments):
        snapshot_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.snapshot)
        documentation_path = tool_arguments.documentation

        documentation = self._get_documentation(documentation_path)

        # create the snapshots
        self._create_snapshots(tool_arguments, snapshot_path, documentation)

        # create the results
        self._create_results(tool_arguments)
    

    def _read_csv(self, filename:str):
        try:
            df = pd.read_csv(filename)
            return df
        except Exception as e:
            logger.error(f'Invalid CSV file ({filename}): {e}')
            raise
        
    def _to_json(self, filename:str, content:dict):
        try:
            with open(filename, 'w') as f:
                json.dump(content, f)
        except Exception as e:
            logger.error(f'Cannot save the file \'{filename}\' as json: {e}')
            raise

    def _process_directory(self, directory: str, snapshot_path: str, df_processing_method):
        logger.info(f'Scanning dir: \'{directory}\'')
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(".csv"):
                    full_path = os.path.join(dirpath, filename)
                    self._process_file(full_path, snapshot_path, df_processing_method)

    def _process_file(self, full_path:str, snapshot_path:str, df_processing_method):
        logger.info(f'Processing file {full_path}')
        df = self._read_csv(full_path)
        df_processing_method(full_path, df, snapshot_path, id=self._tmp_snapshot_id)
        self._tmp_snapshot_id += 1

    # snapshot methods
    def _process_dataframe_to_row_null_distribution_snapshot(self, file_path: str, df: pd.DataFrame, snapshot_path: str, id:int=0):
        """
        Process a dataframe to extract row null distribution and save it as a snapshot.

        ## Parameters
        - filename: The name of the source file.
        - df: The dataframe to be processed.
        - snapshot_path: Path to save the snapshot.
        """
        try:
            result = {'type':CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot, 'id': id, 'file_path': file_path, 'snapshot': dict()}
            for num_of_nulls in df.isnull().sum(axis=1):
                result['snapshot'][num_of_nulls] = result['snapshot'].get(num_of_nulls, 0) + 1

            # specify the output file path
            output_file = os.path.join(snapshot_path, ''.join([CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot, str(id), '.json']))

            self._to_json(output_file, result)
            logger.info(f'\'{os.path.basename(output_file)}\' created!')
        except Exception as e:
            logger.error(f'Error while processing the file ({file_path}): {e}')

    def _create_row_null_distribution_snapshot(self, dataset: list[str], snapshot_path: str, documentation:Documentation):
        logger.info('Creating Row Null Distribution Snapshot')
        logger.info('Creating intermediate results')
        df_processing_method = self._process_dataframe_to_row_null_distribution_snapshot
        self._tmp_snapshot_id = 0
        self._loop_through_dataset(dataset, snapshot_path, df_processing_method)
        self._tmp_snapshot_id = 0

    def _loop_through_dataset(self, dataset:list[str], snapshot_path:str, df_processing_method):
        for file_or_dir in dataset:
            file_or_dir = os.path.abspath(file_or_dir)
            if os.path.isdir(file_or_dir):
                self._process_directory(file_or_dir, snapshot_path, df_processing_method)
            else:
                self._process_file(file_or_dir, snapshot_path, df_processing_method)
