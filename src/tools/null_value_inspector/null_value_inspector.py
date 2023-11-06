import os
import logging
import json

from tools.base_tool import  BaseToolClass
from globals.types import SnapshotType
from tools.null_value_inspector.model.tool_arguments import ToolArguments
from tools.null_value_inspector.model.documentation import Documentation
from logger.utils import log_footer, log_header, get_custom_logger_name

# tools
from tools.null_value_inspector.result_generator.null_distribution_by_row.generator import NullDistributionByRowOverviewGenerator
from tools.null_value_inspector.result_generator.statistical_summary.generator import StatisticalSummaryOverviewGenerator
from tools.null_value_inspector.result_generator.ranked_null_count_by_column.generator import RankedNullCountByColumnOverviewGenerator
from tools.null_value_inspector.result_generator.null_frequent_pairs.generator import NullFrequentPairsOverviewGenerator
from utils.file_operations import FileOperations

# snapshots
from tools.null_value_inspector.snapshot.row_null_distribution.row_null_distribution_snapshot import RowNullDistributionSnapshot
from tools.null_value_inspector.snapshot.column_null_count.columns_null_count_snapshot import ColumnNullCountSnapshot
from tools.null_value_inspector.snapshot.column_pair_null_pattern.column_pair_null_pattern_snapshot import ColumnPairNullPatternSnapshot

logger = logging.getLogger(get_custom_logger_name(__name__))



class NullValueInspector(BaseToolClass):
    _row_null_distribution_snapshot_path:str | None
    _column_null_count_snapshot_path:str | None
    _column_pair_null_pattern_snapshot_path:str | None
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
        except Exception as e:
            logger.info(f'No documentation provided: {e}')
            documentation = Documentation(**dict())
        return documentation
    

    def _create_snapshots(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_snapshot_path)
        log_header(logger, 'Initializing Snapshots')
        if self._row_null_distribution_snapshot_is_necessary(tool_arguments):
            try:
                rowNullDistributionSnapshot = RowNullDistributionSnapshot(self._documentation)
                rowNullDistributionSnapshot.create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._samples)
                self._row_null_distribution_snapshot_path = os.path.join(self._base_snapshot_path, rowNullDistributionSnapshot.get_filename())
            except Exception as e:
                self._logger.error(e)
                raise
        if self._column_null_count_snapshot_is_necessary(tool_arguments):
            try:
                columnNullCountSnapshot = ColumnNullCountSnapshot(self._documentation)
                columnNullCountSnapshot.create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._samples)
                self._column_null_count_snapshot_path = os.path.join(self._base_snapshot_path, columnNullCountSnapshot.get_filename())
            except Exception as e:
                self._logger.error(e)
                raise
        if self._column_pair_null_pattern_snapshot_is_necessary(tool_arguments):
            try:
                columnPairNullPatternSnapshot = ColumnPairNullPatternSnapshot(self._documentation)
                columnPairNullPatternSnapshot.create_snapshot(tool_arguments.dataset, self._base_snapshot_path, self._samples)
                self._column_pair_null_pattern_snapshot_path = os.path.join(self._base_snapshot_path, columnPairNullPatternSnapshot.get_filename())
            except Exception as e:
                self._logger.error(e)
                raise
        log_footer(logger, 'Snapshots Finished    ')
    

    def _column_null_count_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.statistical_summary_overview or tool_arguments.ranked_null_count_by_column_overview

    def _row_null_distribution_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.null_distribution_by_row_overview or tool_arguments.statistical_summary_overview
    
    def _column_pair_null_pattern_snapshot_is_necessary(self, tool_arguments:ToolArguments)->bool:
        return tool_arguments.null_frequent_pairs_overview

    def _create_results(self, tool_arguments:ToolArguments):
        self._file_operations.create_directory(self._base_result_path)
        log_header(logger, 'Initializing Results')
        # TODO refactor: extract repeated code from those ifs
        if tool_arguments.statistical_summary_overview:
            overview_name = 'summary_overview'
            logger.info(f'Creating {overview_name}')
            if self._row_null_distribution_snapshot_path and os.path.isfile(self._row_null_distribution_snapshot_path) and self._column_null_count_snapshot_path and os.path.isfile(self._column_null_count_snapshot_path):
                try:
                    snapshot_path_map = {
                        SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT: self._row_null_distribution_snapshot_path, 
                        SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT: self._column_null_count_snapshot_path,
                    }
                    StatisticalSummaryOverviewGenerator(snapshot_path_map).generate_overview(self._base_result_path)
                except Exception as e:
                    logger.error(f'Error while executing {overview_name}: {e}')
            else:
                logger.error('Invalid row_null_distribution_snapshot or columns_null_count_snapshot')
        if tool_arguments.null_distribution_by_row_overview:
            overview_name = 'null_distribution_by_row_overview'
            logger.info(f'Creating {overview_name}')
            if self._row_null_distribution_snapshot_path and os.path.isfile(self._row_null_distribution_snapshot_path):
                try:
                    snapshot_path_map = {
                        SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT: self._row_null_distribution_snapshot_path, 
                    }
                    NullDistributionByRowOverviewGenerator(snapshot_path_map).generate_overview(self._base_result_path) 
                except Exception as e:
                    logger.error(f'Error while executing {overview_name}: {e}')
            else:
                logger.error('Invalid row_null_distribution_snapshot')
        if tool_arguments.ranked_null_count_by_column_overview:
            overview_name = 'ranked_null_count_by_column_overview'
            logger.info(f'Creating {overview_name}')
            if self._column_null_count_snapshot_path and os.path.isfile(self._column_null_count_snapshot_path):
                try:
                    snapshot_path_map = {
                        SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT: self._column_null_count_snapshot_path, 
                    }
                    RankedNullCountByColumnOverviewGenerator(snapshot_path_map).generate_overview(self._base_result_path)
                except Exception as e:
                    logger.error(f'Error while executing {overview_name}: {e}')
            else:
                logger.error('Invalid column_null_count_snapshot')
        if tool_arguments.null_frequent_pairs_overview:
            overview_name = 'null_frequent_pairs_overview'
            logger.info(f'Creating {overview_name}')
            if self._column_pair_null_pattern_snapshot_path and os.path.isfile(self._column_pair_null_pattern_snapshot_path):
                try:
                    snapshot_path_map = {
                        SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT: self._column_pair_null_pattern_snapshot_path, 
                    }
                    NullFrequentPairsOverviewGenerator(snapshot_path_map).generate_overview(self._base_result_path)
                except Exception as e:
                    logger.error(f'Error while executing {overview_name}: {e}')
            else:
                logger.error('Invalid column_pair_null_pattern_snapshot')
        log_footer(logger, 'Results Finished    ')
    



