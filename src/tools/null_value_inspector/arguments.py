from argparse import ArgumentParser 

def add_arguments(tool_subparser:ArgumentParser):
    null_value_inspector_group = tool_subparser.add_argument_group('Tool: Null Value Inspector Settings')
    null_value_inspector_group.add_argument("hello-world", type=str, help="Hello World")