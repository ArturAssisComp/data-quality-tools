from argparse import ArgumentParser 

def add_arguments(tool_subparser:ArgumentParser):
    null_value_inspector_group = tool_subparser.add_argument_group('Tool: Null Value Inspector Settings')
    null_value_inspector_group.add_argument(
                                            '--null-distribution-by-row-overview', 
                                            '--ndbro', 
                                            '-n0', 
                                            action='store_true', 
                                            default=False,
                                            help="""
                                                Format: Bar Chart | 
                                                Description: Visualizes row counts by null values | 
                                                Axes: X = Null values/row, Y = Row count | 
                                                Snapshot: 'row_null_distribution_snapshot' | 
                                                Insight: Understand null value spread across rows
                                                """)
