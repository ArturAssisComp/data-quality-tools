from src.manager.models.input_interface import InputInterface, Documentation



# implement using pytest
class TestInputInterface:
    def test_input_interface(self):
        input_interface = InputInterface(
            id=1,
            name="test",
            description="test",
            dataset=['file1', 'file2'],
            documentation=Documentation( id=12 ),
            tools_arguments={'tool1': ['arg1', 'arg2'], 'tool2': []},
            )
        assert input_interface.id == 1
        assert input_interface.name == "test"
        assert input_interface.description == "test"
        assert input_interface.dataset == ['file1', 'file2']
        assert input_interface.documentation == Documentation( id=12 )
        assert input_interface.tools_arguments == {'tool1': ['arg1', 'arg2'], 'tool2': []}
