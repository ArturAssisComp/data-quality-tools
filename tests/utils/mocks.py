from src.manager.models.manager_arguments import ManagerArguments
from unittest.mock import patch


@patch('os.path.isfile', return_value=True)
@patch('os.path.isdir', return_value=True)
def get_mock_manager_arguments(mock_isfile, mock_isdir)->ManagerArguments:
    return ManagerArguments(
        name='test',
        description='test',
        dataset=['file1', 'file2'],
        output_path='output_path'
    )