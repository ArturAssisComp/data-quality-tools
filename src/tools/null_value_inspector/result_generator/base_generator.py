import logging
from globals.types import SnapshotType

from logger.utils import get_custom_logger_name
from tools.null_value_inspector.snapshot.model.snapshot_model import SnapshotModel
from utils.file_operations import FileOperations

logger = logging.getLogger(get_custom_logger_name(__name__, len(__name__.split('.')) - 2, 'last'))
class BaseOverviewGenerator:
    _logger:logging.Logger
    _fileOperations:FileOperations
    _snapshots:dict[SnapshotType, SnapshotModel | None]
    def __init__(self, snapshot_filepath:dict[SnapshotType, str], logger:logging.Logger = logger, fileOperations:FileOperations=FileOperations()):
        self._logger = logger
        self._fileOperations = fileOperations
        self._get_snapshots(snapshot_filepath)
    
    def generate_overview(self, basedir_path:str):
        self._logger.info('Creating overview')
        self._generate_specific_overview(basedir_path)
    
    def _get_snapshots(self, snapshot_filepath:dict[SnapshotType, str]):
        self._snapshots = dict()
        for snapshot_type, file_path in snapshot_filepath.items():
            self._snapshots[snapshot_type] = SnapshotModel(** self._fileOperations.read_Json(file_path))
    
    def _generate_specific_overview(self, basedir_path:str):
        raise NotImplementedError('should Implement')


