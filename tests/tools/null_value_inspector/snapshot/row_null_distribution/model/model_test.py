import pytest
import pydantic
from tools.null_value_inspector.snapshot.row_null_distribution.model.model import RowNullDistributionSnapshotModel


ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE = 'row_null_distribution_snapshot'
class TestRowNullDistributionSnapshotModel:
    @pytest.mark.parametrize("_id, input_dict, isValid", [
        ('ValidationError: invalid \'type\'', {
            'type':'other type',
            'files':[],
            'content':{0:12},
            }, False),
        ('ValidationError: invalid \'files\'', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[123],
            'content':{0:12},
            }, False),
        ('ValidationError: invalid \'content\'', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[],
            'content':{'invalid key':12},
            }, False),
        ('ValidationError: empty content', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[],
            'content':{},
            }, False),
        ('empty files', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[],
            'content':{0:12},
            }, True),
        ('1 files and 2 contents', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':[],
            'content':{0:2, 1:4} # 2 rows with 0 nulls, and 4 rows with 1 null
            }, True),
        ('2 files and 1 content', {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1', 'file2'],
            'content':{2:1},
            }, True),
    ])
    def test_row_null_distribution_snapshot(self, _id, input_dict:dict, isValid:bool):
        if isValid:
            result = RowNullDistributionSnapshotModel(**input_dict)
            assert len(result.model_dump()) == 5
            assert result.type == ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE
            assert set(input_dict['files']) == set(result.files)
            assert input_dict['content'] == result.content
            assert result.state == 'initial'
            assert result.num_of_columns == None
        else:
            with pytest.raises(pydantic.ValidationError):
                RowNullDistributionSnapshotModel(**input_dict)
    
    def test_initialize_with_content_key_as_str(self):
        result = RowNullDistributionSnapshotModel(**{
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, '1':4} # 2 rows with 0 nulls, and 4 rows with 1 null
        })
        assert result.model_dump() == {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, 1:4}, # 2 rows with 0 nulls, and 4 rows with 1 null
            'state':'initial',
            'num_of_columns':None,
        }

    def test_update_the_content(self):
        result = RowNullDistributionSnapshotModel(**{
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, 1:4},
            'state':'initial',
            'num_of_columns':None,
        })
        assert result.model_dump() == {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:2, 1:4}, # 2 rows with 0 nulls, and 4 rows with 1 null
            'state':'initial',
            'num_of_columns':None,
        }
        result.content[0] += 1
        result.content[34] = 12

        assert result.model_dump() == {
            'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
            'files':['file1'],
            'content':{0:3, 1:4, 34:12}, # 2 rows with 0 nulls, and 4 rows with 1 null
            'state':'initial',
            'num_of_columns':None,
        }
    
    class TestGetBasicInstance:
        def test_manipulate_basic_instance(self):
            basic_instance = RowNullDistributionSnapshotModel.get_basic_instance()
            assert basic_instance.model_dump() == {
                'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
                'files':[],
                'content':{0:0},
                'state':'initial',
                'num_of_columns':None,
            }
            basic_instance.content = dict()
            assert basic_instance.model_dump() == {
                'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
                'files':[],
                'content':{},
                'state':'initial',
                'num_of_columns':None,
            }
            basic_instance.files.append('file1')
            basic_instance.content[0] = 1
            basic_instance.content[10] = 2
            assert basic_instance.model_dump() == {
                'type':ROW_NULL_DISTRIBUTION_SNAPSHOT_TYPE,
                'files':['file1'],
                'content':{0:1, 10:2},
                'state':'initial',
                'num_of_columns':None,
            }
