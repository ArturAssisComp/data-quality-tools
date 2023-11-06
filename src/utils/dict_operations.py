
def init_column_pair(col1: str, col2: str, content: dict[str, dict]) -> None:
    """
    Initializes the dictionary structure for a pair of columns if they don't already exist.

    Parameters:
    col1 (str): The first column name.
    col2 (str): The second column name.
    content (dict): The dictionary to initialize.
    """
    if col1 not in content:
        content[col1] = {}
    if col2 not in content:
        content[col2] = {}
    
    content[col1].setdefault(col2, 0)
    content[col2].setdefault(col1, 0)