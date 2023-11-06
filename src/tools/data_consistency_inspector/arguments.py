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