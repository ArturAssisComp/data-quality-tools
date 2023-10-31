from argparse import _ArgumentGroup

def add_arguments(manager_group: _ArgumentGroup):
    """
    Adds arguments to the given argument group for manager settings.
    
    ## Arguments added:
    - --name, -n
    - --description
    - --documentation, --doc
    - --dataset, -d
    - --output-path, -o
    """
    manager_group.add_argument("--name", '-n', type=str, default='', help="The name of the query.")

    manager_group.add_argument("--sample", '-s', type=str, default='', help="Specify a sampling strategy for the dataset. Accepts a percentage (e.g., '10%%'), a single integer (e.g., '1000' for 1000 rows), or a combination of percentages and integers (e.g., '12%%, 1024, 234, 100') to generate multiple samples.")

    
    manager_group.add_argument("--description", type=str, default='', help="The description of the query.")
    
    manager_group.add_argument("--documentation", "--doc", type=str, default='',  
                               help="The documentation for the query. Must be a JSON or YAML file. "
                                    "If no file is provided, the analysis will proceed without documentation. "
                                    "Note: Not all tools accept undocumented analysis.")
    
    manager_group.add_argument("--dataset", '-d', type=str, default='.', 
                               help="Paths to datasets. Items can be a folder or a file. "
                                    "For multiple files, use the format 'path1.csv path2.csv ...'. "
                                    "Files must be in CSV format. Default is './'")
    
    manager_group.add_argument("--output-path", '-o', type=str, default=".", 
                               help="Path to the output folder. Default is './'")
