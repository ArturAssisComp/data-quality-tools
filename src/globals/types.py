from enum import Enum


class SnapshotType(Enum):
    ROW_NULL_DISTRIBUTION_SNAPSHOT = 'row_null_distribution_snapshot'
    COLUMN_NULL_COUNT_SNAPSHOT = 'column_null_count_snapshot'
    COLUMN_PAIR_NULL_PATTERN_SNAPSHOT = 'column_pair_null_pattern_snapshot'

def get_snapshot_filename(type:SnapshotType):
    return type.value.replace('_', '-')