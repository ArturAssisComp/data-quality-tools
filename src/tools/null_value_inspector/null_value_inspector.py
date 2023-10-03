from globals.interfaces import BaseToolClass
from globals.constants import CONSTANTS
from tools.null_value_inspector.model.tool_arguments import ToolArguments
from tools.null_value_inspector.model.documentation import Documentation
import pandas as pd
import os
import logging
import json

logger = logging.getLogger(__name__)



class NullValueInspector(BaseToolClass):

    @staticmethod
    def _get_documentation(documentation_path:str):
        try:
            with open(documentation_path, 'r') as f:
                # Load JSON data from file
                data = json.load(f)
                documentation = Documentation(**data)
        except Exception as e:
            logger.info(f'No documentation provided: {e}')
            documentation = Documentation(**dict())
        return documentation
    
    @staticmethod
    def _create_snapshot_directory(snapshot_path:str):
        try:
            if not os.path.isdir(snapshot_path):
                os.makedirs(snapshot_path)
        except Exception as e:
            logger.error(f'Not able to create directories for snapshot path: {e}')
            raise
        logger.info('Snapshot directory created!')


    @classmethod
    def _create_snapshots(cls, tool_arguments:ToolArguments, snapshot_path:str, documentation:Documentation):
        if tool_arguments.null_distribution_by_row_overview:

            logger.info('Creating row_null_distribution_snapshot')
            cls._create_snapshot_directory(snapshot_path)
            cls._create_row_null_distribution_snapshot(tool_arguments.dataset, snapshot_path, documentation)
    
    @classmethod
    def _create_results(cls, tool_arguments:ToolArguments):
        if tool_arguments.null_distribution_by_row_overview:
            logger.info('Creating null-distribution-by-row-overview')


    @classmethod
    def work_on(cls, tool_arguments: ToolArguments):
        snapshot_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.snapshot)
        documentation_path = tool_arguments.documentation

        documentation = cls._get_documentation(documentation_path)

        # create the snapshots
        cls._create_snapshots(tool_arguments, snapshot_path, documentation)

        # create the results
        cls._create_results(tool_arguments)
    

    @staticmethod
    def _read_csv(filename:str):
        try:
            df = pd.read_csv(filename)
            return df
        except Exception as e:
            logger.error(f'Invalid CSV file ({filename}): {e}')
            raise
        
    @staticmethod
    def _to_json(filename:str, content:dict):
        try:
            with open(filename, 'w') as f:
                json.dump(content, f)
        except Exception as e:
            logger.error(f'Cannot save the file \'{filename}\' as json: {e}')
            raise
    @classmethod
    def _process_directory(cls, directory: str, snapshot_path: str, df_processing_method):
        logger.info(f'Processing dir {directory}')
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(".csv"):
                    full_path = os.path.join(dirpath, filename)
                    df = cls._read_csv(full_path)
                    df_processing_method(full_path, df, snapshot_path)

    # snapshot methods
    @classmethod
    def _process_dataframe_to_row_null_distribution_snapshot(cls, filename: str, df: pd.DataFrame, snapshot_path: str, id:int=0):
        """
        Process a dataframe to extract row null distribution and save it as a snapshot.

        ## Parameters
        - filename: The name of the source file.
        - df: The dataframe to be processed.
        - snapshot_path: Path to save the snapshot.
        """
        try:
            result = {'type':CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot, 'id': id, 'filename': filename, 'snapshot': dict()}
            for num_of_nulls in df.isnull().sum(axis=1):
                result['snapshot'][num_of_nulls] = result['snapshot'].get(num_of_nulls, 0) + 1

            # specify the output file path
            output_file = os.path.join(snapshot_path, ''.join([CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot, str(id), '.json']))

            cls._to_json(output_file, result)
        except Exception as e:
            logger.error(f'Error while processing the file ({filename}): {e}')

    @classmethod
    def _create_row_null_distribution_snapshot(cls, dataset: list[str], snapshot_path: str, documentation:Documentation):
        logger.info('Creating Row Null Distribution Snapshot')
        logger.info('Creating intermediate results')
        for file_or_dir in dataset:
            if os.path.isdir(file_or_dir):
                cls._process_directory(file_or_dir, snapshot_path, cls._process_dataframe_to_row_null_distribution_snapshot)
            else:
                logger.info(f'Processing file {file_or_dir}')
                df = cls._read_csv(file_or_dir)
                cls._process_dataframe_to_row_null_distribution_snapshot(file_or_dir, df, snapshot_path, id=0)
