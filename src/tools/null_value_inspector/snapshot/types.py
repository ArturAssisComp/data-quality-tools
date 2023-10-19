from typing import Literal

Snapshot = Literal['row_null_distribution_snapshot', 'column_null_count_snapshot', 'column_pair_null_pattern']
State = Literal['initial', 'free-mode', 'strict-mode', 'subset-mode']
