from re import L
import py
import pytest

from pre_commit_dbt.check_model_has_keys import main

COLUMNS = """version: 2

models:
    - name: model_with_columns_1
      columns:
    - name: model_with_columns_2
      columns:
"""

NO_COLUMNS = """version: 2

models:
    - name: model_without_columns_1
    - name: model_without_columns_2
"""

MIXED_COLUMNS = """version: 2

models:
    - name: model_with_columns
      columns:
    - name: model_without_columns
"""

def gen_test_schema_file(schema, file_name, tmpdir) -> str:

    yml_file_path = tmpdir.join(f"{file_name}")
    yml_file_path_str = str(yml_file_path)

    with open(yml_file_path, 'w+'):
        yml_file_path.write(schema)

    return yml_file_path_str


@pytest.mark.parametrize(
    "schema_yaml, keys, expected_status_code",
    [
        pytest.param(COLUMNS, ["columns"], 0, id="target_key_present"),
        pytest.param(NO_COLUMNS, ["columns"], 1, id="target_key_missing"),
        pytest.param(MIXED_COLUMNS, ["columns"], 1, id="some_target_keys_missing"),
        pytest.param(COLUMNS, ["random"], 1, id="target_key_not_present"),
        pytest.param(COLUMNS,["columns","random"], 1, id="some_target_keys_missing_2"),
    ]
)
def test_check_model_keys(schema_yaml, keys, expected_status_code, tmpdir):

    schema_file = gen_test_schema_file(schema_yaml, 'test_schema.yml', tmpdir)

    args = []
    keys.insert(0, '--keys')
    args.extend(keys)
    args.insert(0, schema_file)

    status_code = main(
        argv=args,
    )
    assert status_code == expected_status_code
