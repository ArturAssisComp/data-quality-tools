import argparse
from tools.null_value_inspector.arguments import add_arguments as null_value_inspector_add_arguments
from manager.arguments import add_arguments as manager_add_arguments

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
    null_value_inspector_parser = subparsers.add_parser("null-value-inspector", aliases=["nvi"], help="Null Value Inspector")
    null_value_inspector_add_arguments(null_value_inspector_parser)

    # new-tool tool subparser
    # new_tool_parser = subparsers.add_parser("new-tool", aliases=['nt'], help=" New Tool")
    # new_tool_add_arguments(new_tool_parser)


    # hello world tool subparser
    hello_world_parser = subparsers.add_parser("hello-world", help="Tool: Hello World")
    hello_world_group = hello_world_parser.add_argument_group('Hello World Settings')
    hello_world_group.add_argument("abc", type=str, help="Hello World")

    print('hello')
    args = parser.parse_args()
    print('world')
    print(f'{vars(args)} =')

if __name__ == "__main__":
    main()
