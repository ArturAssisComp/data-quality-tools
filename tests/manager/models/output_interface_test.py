
from src.manager.models.output_interface import OutputInterface 



# implement using pytest
class TestOutputInterface:
    def test_output_interface(self):
        data_quality_snapshot = '{"test": "test"}'
        data_quality_summary_report = '{"summary": "test"}'
        output_interface = OutputInterface(
            id=1,
            name="test",
            description="test",
            data_quality_snapshot= data_quality_snapshot,
            data_quality_summary_report= data_quality_summary_report
            )
        assert output_interface.id == 1
        assert output_interface.name == "test"
        assert output_interface.description == "test"
        assert output_interface.data_quality_snapshot == {"test": "test"}  
        assert output_interface.data_quality_summary_report == {"summary": "test"}  