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
    @classmethod
    def work_on(cls, tool_arguments: ToolArguments):
        snapshot_path = os.path.join(tool_arguments.output_path, CONSTANTS.FilesFoldersNames.snapshot)

        try:
            documentation_path = tool_arguments.documentation
            with open(documentation_path, 'r') as f:
                # Load JSON data from file
                data = json.load(f)
                documentation = Documentation(**data)
        except Exception as e:
            logger.info(f'No documentation provided: {e}')
            documentation = Documentation(**dict())
    

        # create the snapshots
        if tool_arguments.null_distribution_by_row_overview:

            logger.info('Creating row_null_distribution_snapshot')
            if not os.path.isdir(snapshot_path):
                os.makedirs(snapshot_path)
            cls._create_row_null_distribution_snapshot(tool_arguments.dataset, snapshot_path)

        # create the results
        if tool_arguments.null_distribution_by_row_overview:
            logger.info('Creating null-distribution-by-row-overview')
    
    @classmethod
    def _create_row_null_distribution_snapshot(cls, dataset:list[str], snapshot_path:str):
        logger.info('Creating Row Null Distribution Snapshot')
        for file_or_dir in dataset:
            if os.path.isdir(file_or_dir):
                directory = file_or_dir
                logger.info(f'Processing dir {directory}')
                # TODO implement the provessing for each file in the directory
                pass
            else: # is file
                file = file_or_dir
                logger.info(f'Processing file {file}')
                try:
                    basename = os.path.basename(file).split('.')[0]
                    df = pd.read_csv(file)
                    try:
                        result = {'filename':file, 'snapshot':dict()}
                        for num_of_nulls in df.isnull().sum(axis=1):
                            result['snapshot'][num_of_nulls] = result['snapshot'].get(num_of_nulls, 0) + 1
                        
                        # specify the output file path
                        output_file = os.path.join(snapshot_path, ''.join([CONSTANTS.FilesFoldersNames.row_null_distribution_snapshot, '_', basename, '.json']))

                        # write the result to a JSON file
                        with open(output_file, 'w') as f:
                            json.dump(result, f)
                    except Exception as e:
                        logger.error(f'Error while processing the file ({file}): {e}')
                except:
                    logger.error(f'Invalid CSV file: {file}')


    
