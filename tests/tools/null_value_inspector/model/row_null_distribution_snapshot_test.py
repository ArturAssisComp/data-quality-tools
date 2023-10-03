import pytest
import pydantic
from tools.null_value_inspector.model.row_null_distribution_snapshot import RowNullDistributionSnapshot


ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE = 'row_null_distribution_snapshot'
class TestRowNullDistributionSnapshotModel:
    @pytest.mark.parametrize("_id, input_dict, isValid", [
        ('ValidationError', {
            'type':'other type',
            'files':[],
            'content':{0:12},
            }, False),
        ('ValidationError', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[123],
            'content':{0:12},
            }, False),
        ('ValidationError', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[],
            'content':{'invalid key':12},
            }, False),
        ('empty files', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[],
            'content':{0:12},
            }, True),
        ('1 file', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{2:1},
            }, True),
        ('2 files', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1', 'file2'],
            'content':{2:1},
            }, True),
        ('0 files and 1 content', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[],
            'content':{0:2, 1:4} # 2 rows with 0 nulls, and 4 rows with 1 null
            }, True),
    ])
    def test_row_null_distribution_snapshot(self, _id, input_dict:dict, isValid:bool):
        if isValid:
            result = RowNullDistributionSnapshot(**input_dict)
            assert len(result.model_dump()) == 3
            assert result.type == ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE
            assert set(input_dict['files']) == set(result.files)
            assert input_dict['content'] == result.content
        else:
            with pytest.raises(pydantic.ValidationError):
                RowNullDistributionSnapshot(**input_dict)
    
    def test_initialize_with_content_key_as_str(self):
        result = RowNullDistributionSnapshot(**{
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, '1':4} # 2 rows with 0 nulls, and 4 rows with 1 null
        })
        assert result.model_dump() == {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, 1:4} # 2 rows with 0 nulls, and 4 rows with 1 null
        }

    def test_update_the_content(self):
        result = RowNullDistributionSnapshot(**{
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, 1:4} 
        })
        assert result.model_dump() == {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, 1:4} # 2 rows with 0 nulls, and 4 rows with 1 null
        }
        result.content[0] += 1
        result.content[34] = 12

        assert result.model_dump() == {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:3, 1:4, 34:12} # 2 rows with 0 nulls, and 4 rows with 1 null
        }
