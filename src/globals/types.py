from enum import Enum


class SnapshotType(Enum):
    # null value inspector tool
    ROW_NULL_DISTRIBUTION_SNAPSHOT = 'row_null_distribution_snapshot'
    COLUMN_NULL_COUNT_SNAPSHOT = 'column_null_count_snapshot'
    COLUMN_PAIR_NULL_PATTERN_SNAPSHOT = 'column_pair_null_pattern_snapshot'
    # data inconsistency inspector tool
    ROW_INCONSISTENCY_DISTRIBUTION_SNAPSHOT = 'row_inconsistency_distribution_snapshot'

class SnapshotMode(Enum):
    INITIAL = 'initial'
    FREE_MODE = 'free-mode'
    STRICT_MODE = 'strict-mode'
    SUBSET_MODE = 'subset-mode'


def get_snapshot_name(type:SnapshotType):
    return type.value.replace('_', '-')