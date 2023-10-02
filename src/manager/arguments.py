from argparse import _ArgumentGroup
def add_arguments(manager_group:_ArgumentGroup):
    '''
    ## Arguments added
    - --name, -n
    - --description
    - --documentation, --doc
    - --dataset, -d
    - --output-path, -o
    '''
    manager_group.add_argument("--name", '-n', type=str, default='', help="The name of the query.")
    manager_group.add_argument("--description", type=str, default='', help="The description of the query.")
    manager_group.add_argument("--documentation", "--doc", type=str, default='',  help="The documentation that will be used for the query. The file must be a JSON or YAML. If no file is provided, the analysis will be made without documentation. Not all tools accept that kind of analysis.")
    manager_group.add_argument("--dataset", '-d', type=str, default=['.'], help="Path to datasets. Each item can be a folder or a file. For multiple files use the format \"path1.csv, path2.csv, ...\" if they have some space or only separated by commas if they do not have spaces. For files, the format must be csv. Default is ./")
    manager_group.add_argument("--output-path", '-o', type=str, default=".", help="Path to the output folder. Default is ./")