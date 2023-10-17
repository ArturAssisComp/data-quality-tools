from typing import Literal

Snapshot = Literal['row_null_distribution_snapshot', 'column_null_count_snapshot']
State = Literal['initial', 'free-mode', 'strict-mode', 'subset-mode']
