from argparse import ArgumentParser 

def add_arguments(tool_subparser:ArgumentParser):
    """
    Add arguments for the Null Value Inspector tool.

    Args:
    - tool_subparser (ArgumentParser): ArgumentParser object to which the arguments are added.
    """
    null_value_inspector_group = tool_subparser.add_argument_group(
        'Tool: Null Value Inspector Settings'
    )

    help_text = (
        "Format: JSON | "
        "Description: Multiple metrics that will help assessing the quality of the data in analysis; | "
        "Snapshot: 'row_null_distribution_snapshot', 'column_null_count_snapshot' | "
        "Insight: Statistical insights"
    )

    null_value_inspector_group.add_argument(
        '--statistical-summary-overview',
        '--ss',
        '-n0',
        action='store_true',
        default=False,
        help=help_text
    )

    help_text = (
        "Format: Bar Chart | "
        "Description: Visualizes row counts by null values | "
        "Axes: X = Null values/row, Y = Row count | "
        "Snapshot: 'row_null_distribution_snapshot' | "
        "Insight: Understand null value spread across rows"
    )

    null_value_inspector_group.add_argument(
        '--null-distribution-by-row-overview',
        '--ndbro',
        '-n1',
        action='store_true',
        default=False,
        help=help_text
    )