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
