import argparse
from tools.null_value_inspector.constants import CONSTANTS as NULL_VALUE_INSPECTOR_CONSTANTS 
from tools.null_value_inspector.arguments import add_arguments as null_value_inspector_add_arguments
from manager.arguments import add_arguments as manager_add_arguments
from manager.manager import Manager
from logger.config_logger import configure_logger 
import logging

def main():
    parser = argparse.ArgumentParser(
        description='A toolkit for data quality. It helps you to generate data quality'
                    ' reports about structured data.',
        epilog='For more information, visit https://github.com/ArturAssisComp/data-quality-tools#readme',
    )

    general_group = parser.add_argument_group('General')
    general_group.add_argument("--version", "-v", action="version", version="data-quality-tools 0.0.1")

    # add arguments for the manager
    manager_group = parser.add_argument_group('Manager')
    manager_add_arguments(manager_group)



    # Add subparsers for the tools
    subparsers = parser.add_subparsers(title="Tools", dest="tool_name", description="Available tools for data quality check.")

    # Null Value Inspector tool subparser with alias

    null_value_inspector_parser = subparsers.add_parser(NULL_VALUE_INSPECTOR_CONSTANTS.tool_name, aliases=[NULL_VALUE_INSPECTOR_CONSTANTS.alias], help="Null Value Inspector")
    null_value_inspector_add_arguments(null_value_inspector_parser)

    # new-tool tool subparser
    # new_tool_parser = subparsers.add_parser("new-tool", aliases=['nt'], help=" New Tool")
    # new_tool_add_arguments(new_tool_parser)


    # hello world tool subparser
    hello_world_parser = subparsers.add_parser("hello-world", help="Tool: Hello World")
    hello_world_group = hello_world_parser.add_argument_group('Hello World Settings')
    hello_world_group.add_argument("abc", type=str, help="Hello World")

    args = parser.parse_args()

    if args.tool_name is None:
        print("Error: Please select a tool to run. Use --help or -h to see the available tools.")
        exit(1)

    configure_logger()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting {args.tool_name} tool.")
    try:
        Manager().process_user_request(vars(args))
    except Exception as e:
        print('Error during execution. Check the log file for more information.')
        exit(1)


if __name__ == "__main__":
    main()
