import pytest
from src.manager.models.user_request import UserRequest
from src.manager.models.manager_request import ManagerRequest
from src.manager.models.documentation import Documentation




class TestManagerRequest():

    @pytest.mark.parametrize("user_request", [
        UserRequest(
            id=1,
            name='test',
            description="test",
            dataset=['file1', 'file2'],
            documentation=Documentation(id=23),
            tools_arguments={'tool1': ['arg1', 'arg2'], 'tool2': []},
        ),

        # Different name, description, and dataset
        UserRequest(
            id=2,
            name='testA',
            description="testA",
            dataset=['fileA1', 'fileA2', 'fileA3'],
            documentation=Documentation(id=24),
            tools_arguments={'toolA1': ['argA1', 'argA2'], 'toolA2': ['argA3']},
        ),

        # Multiple tools with varying arguments
        UserRequest(
            id=3,
            name='testB',
            description="testB",
            dataset=['fileB1'],
            documentation=Documentation(id=25),
            tools_arguments={'toolB1': ['argB1', 'argB2', 'argB3'], 'toolB2': ['argB4', 'argB5'], 'toolB3': []},
        ),

        # Single tool and no arguments
        UserRequest(
            id=4,
            name='testC',
            description="testC",
            dataset=['fileC1', 'fileC2', 'fileC3', 'fileC4'],
            documentation=Documentation(id=26),
            tools_arguments={'toolC1': []},
        ),

        # Different documentation id and single tool
        UserRequest(
            id=5,
            name='testD',
            description="testD",
            dataset=['fileD1', 'fileD2'],
            documentation=Documentation(id=30),
            tools_arguments={'toolD1': ['argD1']},
        )
    ])
    def test_from_user_request(self, user_request):
        manager_request = ManagerRequest.from_user_request(user_request)
        assert isinstance(manager_request.id, int)
        assert manager_request.name == user_request.name
        assert manager_request.description == user_request.description

        for n, (key, value) in enumerate(user_request.tools_arguments.items()):
            assert manager_request.requests[n].tool == key
            assert manager_request.requests[n].arguments == value
            assert manager_request.requests[n].dataset == user_request.dataset
            assert manager_request.requests[n].documentation == user_request.documentation
