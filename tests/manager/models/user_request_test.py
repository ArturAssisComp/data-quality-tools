from src.manager.models.user_request import UserRequest 
from src.manager.models.documentation import Documentation
from src.manager.models.manager_arguments import ManagerArguments
from tests.utils.mocks import get_mock_manager_arguments

# implement using pytest
class TestUserRequest:
    def test_input_interface(self):
        input_interface = UserRequest(
            id=1,
            name="test",
            description="test",
            dataset=['file1', 'file2'],
            manager_arguments= get_mock_manager_arguments(),
            documentation=Documentation( id=12 ),
            tools_arguments={'tool1': ['arg1', 'arg2'], 'tool2': []},
            )
        assert input_interface.id == 1
        assert input_interface.name == "test"
        assert input_interface.description == "test"
        assert input_interface.dataset == ['file1', 'file2']
        assert input_interface.documentation == Documentation( id=12 )
        assert input_interface.tools_arguments == {'tool1': ['arg1', 'arg2'], 'tool2': []}
        assert input_interface.manager_arguments == get_mock_manager_arguments()
