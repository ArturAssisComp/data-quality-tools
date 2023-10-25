import logging
from typing import Any
from globals.types import SnapshotType

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.column_null_count.model.model import ColumnNullCountSnapshotContent
from tools.null_value_inspector.snapshot.column_pair_null_pattern.model.model import ColumnPairNullPatternSnapshotContent
from tools.null_value_inspector.snapshot.model.snapshot_model import SnapshotModel
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotContent
from utils.file_operations import FileOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))
class BaseOverviewGenerator:
    _logger:logging.Logger
    _fileOperations:FileOperations
    _snapshots:dict[SnapshotType, SnapshotModel | None]
    _needed_snapshots:list[SnapshotType]
    def __init__(self, snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
        self._get_snapshots(snapshot_filepath)
    
    def generate_overview(self, basedir_path:str):
        self._logger.info('Creating overview')
        self._parse_snapshot(basedir_path)
    
    def _get_snapshots(self, snapshot_filepath:dict[SnapshotType, str]):
        self._snapshots = dict()
        for snapshot_type, file_path in snapshot_filepath.items():
            self._snapshots[snapshot_type] = SnapshotModel(** self._fileOperations.read_Json(file_path))

    def _handle_content(self, parsed_content_dict:dict[SnapshotType, Any], basedir_path:str, name_preffix:str=''):
        raise NotImplementedError('should Implement')

    def _parse_snapshot(self, basedir_path:str):
        snapshot_types = self._needed_snapshots
        snapshot_list:list[SnapshotModel] = []

        for snapshot_type in snapshot_types:
            snapshot = self._snapshots[snapshot_type]
            if snapshot is None:
                self._logger.error(f'Invalid snapshot: {snapshot_type.value}')
                raise RuntimeError('Invalid Snapshot')
            snapshot_list.append(snapshot)

        if all(map(lambda x:x.population is not None,snapshot_list)):
            parsed_content = map(self._get_snapshot_content_callback(), zip(snapshot_list, snapshot_types))
            parsed_content_dict = dict()
            for content, type_ in parsed_content:
                parsed_content_dict[type_] = content
            self._logger.info('processing population')
            self._handle_content(parsed_content_dict, basedir_path)
        elif all(map(lambda x:x.samples is not None,snapshot_list)):
            base_snapshot = snapshot_list[0]
            assert base_snapshot.samples
            for sample_key in base_snapshot.samples:
                parsed_content = map(self._get_snapshot_content_callback(is_population=False, sample_key=sample_key), zip(snapshot_list, snapshot_types))
                parsed_content_dict = dict()
                for content, type_ in parsed_content:
                    parsed_content_dict[type_] = content
                self._logger.info(f'processing sample {sample_key}')
                self._handle_content(parsed_content_dict, basedir_path, name_preffix=f'sample{sample_key.replace('%', 'rel')}-')
        else:
            self._logger.error('Invalid snapshot format')

    def _get_snapshot_content_callback(self, is_population:bool=True, sample_key:str|None=None):
        def _get_snapshot_content(snapshot_value_type:tuple[SnapshotModel, SnapshotType]):
            value, type_ = snapshot_value_type
            if is_population:
                assert value.population
                content = value.population['content']
            elif sample_key:
                assert value.samples
                content = value.samples[sample_key]['content']
            else:
                raise RuntimeError('Invalid state: invalid sample key')
            match type_:
                case SnapshotType.COLUMN_NULL_COUNT_SNAPSHOT:
                    result = ColumnNullCountSnapshotContent(content=content)
                case SnapshotType.COLUMN_PAIR_NULL_PATTERN_SNAPSHOT:
                    result = ColumnPairNullPatternSnapshotContent(content=content)
                case SnapshotType.ROW_NULL_DISTRIBUTION_SNAPSHOT:
                    result = RowNullDistributionSnapshotContent(content=content)
                case _:
                    raise ValueError('Unexpected snapshot type')
            return result, type_
        return _get_snapshot_content


