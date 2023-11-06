import logging
import json
import os

from pydantic import ValidationError
from globals.types import SnapshotType

from tools.base_tool import  BaseToolClass
from tools.data_consistency_inspector.model.tool_arguments import ToolArguments
from tools.data_consistency_inspector.model.documentation import Documentation
from logger.utils import log_footer, log_header, get_custom_logger_name

from utils.file_operations import FileOperations

# tools
from tools.data_consistency_inspector.result_generator.inconsistency_distribution_by_row.generator import InconsistencyDistributionByRowOverviewGenerator
from tools.data_consistency_inspector.result_generator.ranked_inconsistency_count_by_column.generator import RankedInconsistencyCountByColumnOverviewGenerator
from tools.data_consistency_inspector.result_generator.inconsistent_frequent_pairs.generator import InconsistentFrequentPairsOverviewGenerator

# snapshots
from tools.data_consistency_inspector.snapshot.row_inconsistency_distribution.row_inconsistency_distribution_snapshot import RowInconsistencyDistributionSnapshot
from tools.data_consistency_inspector.snapshot.column_inconsistency_count_by_type.column_inconsistency_count_by_type_snapshot import ColumnInconsistencyCountByTypeSnapshot
from tools.data_consistency_inspector.snapshot.column_pair_inconsistency_pattern.column_pair_inconsistency_pattern_snapshot import ColumnPairInconsistencyPatternSnapshot

logger = logging.getLogger(get_custom_logger_name(__name__))



class DataConsistencyInspector(BaseToolClass):
    _row_inconsistency_distribution_snapshot_path:str|None
    _column_inconsistency_count_by_type_snapshot_path:str|None
    _column_pair_inconsistency_pattern_snapshot_path:str|None
    _documentation:Documentation
    def __init__(self, logger:logging.Logger = logger, file_operations:FileOperations=FileOperations()):
        self._file_operations = file_operations
        self._logger = logger

    def _get_documentation(self, documentation_path:str):
        """
        Retrieves the documentation from the provided path.
        """
        try:
            with open(documentation_path, 'r') as f:
                # Load JSON data from file
                data = json.load(f)
                documentation = Documentation(**data)
                logger.info(f'Documentation read: {documentation}')
        except FileNotFoundError as e:
            self._logger.info(f'No documentation provided: {e}')
            raise
        except ValidationError as e:
            self._logger.info(f'Invalid documentation: {e}')
            raise
        except Exception as e:
            self._logger.info(f'Error while reading documentation: {e}')
            raise
        return documentation
    

    def _create_snapshots(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_snapshot_path)
        log_header(logger, 'Initializing Snapshots')
        if self._row_inconsistency_distribution_snapshot_is_necessary(tool_arguments):
            try:
                rowInconsistencyDistributionSnapshot = RowInconsistencyDistributionSnapshot(self._documentation)
                rowInconsistencyDistributionSnapshot.create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._samples)
                self._row_inconsistency_distribution_snapshot_path = os.path.join(self._base_snapshot_path, rowInconsistencyDistributionSnapshot.get_filename())
            except Exception as e:
                self._logger.error(e)
                raise
        if self._column_inconsistency_count_by_type_snapshot_is_necessary(tool_arguments):
            try:
                columnInconsistencyCountByTypeSnapshot = ColumnInconsistencyCountByTypeSnapshot(self._documentation)
                columnInconsistencyCountByTypeSnapshot.create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._samples)
                self._column_inconsistency_count_by_type_snapshot_path = os.path.join(self._base_snapshot_path, columnInconsistencyCountByTypeSnapshot.get_filename())
            except Exception as e:
                self._logger.error(e)
                raise
        if self._column_pair_inconsistency_pattern_snapshot_is_necessary(tool_arguments):
            try:
                columnPairInconsistencyPatternSnapshot = ColumnPairInconsistencyPatternSnapshot(self._documentation)
                columnPairInconsistencyPatternSnapshot .create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._samples)
                self._column_pair_inconsistency_pattern_snapshot_path = os.path.join(self._base_snapshot_path, columnPairInconsistencyPatternSnapshot.get_filename())
            except Exception as e:
                self._logger.error(e)
                raise
        log_footer(logger, 'Snapshots Finished    ')
    
    def _row_inconsistency_distribution_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.inconsistency_distribution_by_row_overview
    
    def _column_inconsistency_count_by_type_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.ranked_inconsistency_count_by_column_overview

    def _column_pair_inconsistency_pattern_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.inconsistent_frequent_pairs_overview

    def _create_results(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_result_path)
        log_header(logger, 'Initializing Results')
        if tool_arguments.inconsistency_distribution_by_row_overview:
            overview_name = 'inconsistency_distribution_by_row_overview'
            logger.info(f'Creating {overview_name}')
            if self._row_inconsistency_distribution_snapshot_path and os.path.isfile(self._row_inconsistency_distribution_snapshot_path):
                try:
                    snapshot_path_map = {
                        SnapshotType.ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT: self._row_inconsistency_distribution_snapshot_path, 
                    }
                    InconsistencyDistributionByRowOverviewGenerator(snapshot_path_map).generate_overview(self._base_result_path) 
                except Exception as e:
                    logger.error(f'Error while executing {overview_name}: {e}')
            else:
                logger.error('Invalid row_inconsistency_distribution_snapshot')
        if tool_arguments.ranked_inconsistency_count_by_column_overview:
            overview_name = 'ranked_inconsistency_count_by_column_overview'
            logger.info(f'Creating {overview_name}')
            if self._column_inconsistency_count_by_type_snapshot_path and os.path.isfile(self._column_inconsistency_count_by_type_snapshot_path):
                try:
                    snapshot_path_map = {
                        SnapshotType.COLUMN_INCONSISTENCY_COUNT_BY_TYPE_SNAPSHOT: self._column_inconsistency_count_by_type_snapshot_path, 
                    }
                    RankedInconsistencyCountByColumnOverviewGenerator(snapshot_path_map).generate_overview(self._base_result_path) 
                except Exception as e:
                    logger.error(f'Error while executing {overview_name}: {e}')
            else:
                logger.error('Invalid column_inconsistency_count_by_type_snapshot')
        if tool_arguments.inconsistency_distribution_by_row_overview:
            overview_name = 'inconsistency_distribution_by_row_overview'
            logger.info(f'Creating {overview_name}')
            if self._column_pair_inconsistency_pattern_snapshot_path and os.path.isfile(self._column_pair_inconsistency_pattern_snapshot_path):
                try:
                    snapshot_path_map = {
                        SnapshotType.COLUMN_PAIR_INCONSISTENCY_PATTERN_SNAPSHOT: self._column_pair_inconsistency_pattern_snapshot_path,
                    }
                    InconsistentFrequentPairsOverviewGenerator(snapshot_path_map).generate_overview(self._base_result_path)
                except Exception as e:
                    logger.error(f'Error while executing {overview_name}: {e}')
            else:
                logger.error('Invalid column_pair_inconsistency_pattern_snapshot')

        log_footer(logger, 'Results Finished    ')
    



