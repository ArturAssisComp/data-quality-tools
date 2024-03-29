from argparse import ArgumentParser 

def add_arguments(tool_subparser:ArgumentParser):
    """
    Add arguments for the Data Consistency Inspector tool.

    Args:
    - tool_subparser (ArgumentParser): ArgumentParser object to which the arguments are added.
    """
    data_consistency_inspector_group = tool_subparser.add_argument_group(
        'Tool: Data Consistency Inspector Settings'
    )


    help_text = (
        "Format: JSON | "
        "Description: Multiple metrics that will help assessing the quality of the data in analysis; | "
        "Snapshot: 'row_inconsistency_distribution_snapshot', 'column_inconsistency_count_by_type_snapshot' | "
        "Insight: Statistical insights"
    )

    data_consistency_inspector_group.add_argument(
        '--statistical-summary-overview',
        '--sso',
        '-n0',
        action='store_true',
        default=False,
        help=help_text
    )



    help_text = (
        "Format: Bar Chart | "
        "Description: Visualizes row counts by inconsistency values | "
        "Axes: X = Inconsistent values/row, Y = Row count | "
        "Snapshot: 'row_inconsistency_distribution_snapshot' | "
        "Insight: Understand inconsistency values spread across rows"
    )

    data_consistency_inspector_group.add_argument(
        '--inconsistency-distribution-by-row-overview',
        '--idbro',
        '-n1',
        action='store_true',
        default=False,
        help=help_text
    )

    help_text = (
        "Format: Bar Chart | "
        "Description: Visualizes inconsistencies by column, ranked from the greatest to the smallest | "
        "Axes: X = Column name, Y = Inconsistency count or Y = Percentage of Inconsistencies  | "
        "Snapshot: 'column_inconsistency_count_by_type_snapshot' | "
        "Insight: identify columns needing attention based on inconsistency data"
    )

    data_consistency_inspector_group.add_argument(
        '--ranked-inconsistency-count-by-column-overview',
        '--ricbco',
        '-n2',
        action='store_true',
        default=False,
        help=help_text
    )



    help_text = (
        "Format: Heatmap | "
        "Description: Ranks frequent combinations of pairs of columns with inconsistencies | "
        "Snapshot: 'column_pair_inconsistency_pattern_snapshot' | "
        "Insight: Highlight potential correlation between two columns in terms of inconsistency problems"
    )

    data_consistency_inspector_group.add_argument(
        '--inconsistent-frequent-pairs-overview',
        '--ifpo',
        '-n3',
        action='store_true',
        default=False,
        help=help_text
    )

    help_text = (
        "Format: Bar Chart | "
        "Description: Visualizes inconsistencies by column and by type of inconsistency, ranked from the greatest to the smallest;"
        "Axes: X = Column name (first level) and Inconsistency type name (second level), Y = Inconsistency count or Y = Percentage of inconsistencies;"
        "Snapshot: 'column_inconsistency_count_by_type_snapshot' | "
        "Insight: identify columns needing attention based on inconsistency data"
    )

    data_consistency_inspector_group.add_argument(
        '--ranked-inconsistency-count-by-type-and-column-overview',
        '--ricbtco',
        '-n4',
        action='store_true',
        default=False,
        help=help_text
    )
