import pytest

from pre_commit_dbt.check_model_materialized import main


TESTS = (
    (["aa/bb/with_materialized.sql", "--materialized", "view", "table"], True, 0),
    (["aa/bb/with_materialized_table.sql", "--materialized", "table"], True, 0),
    (["aa/bb/with_materialized_table.sql", "--materialized", "view"], True, 1),
    (["aa/bb/with_materialized_empty.sql", "--materialized", "view"], True, 1),
    (["aa/bb/without_materialized.sql", "--materialized", "view"], True, 1)
)

@pytest.mark.parametrize(
    ("input_args", "valid_manifest", "expected_status_code"), TESTS
)
def test_check_model_materialized(
    input_args, valid_manifest, expected_status_code, manifest_path_str
):
    if valid_manifest:
        input_args.extend(["--manifest", manifest_path_str])
    status_code = main(input_args)
    assert status_code == expected_status_code


def test_check_model_materialized_in_changed(tmpdir, manifest_path_str):
    schema_yml = """
version: 2

models:
-   name: in_schema_materialized
    materialized: view
-   name: xxx
    """
    yml_file = tmpdir.join("schema.yml")
    yml_file.write(schema_yml)
    result = main(
        argv=[
            "in_schema_materialized.sql",
            str(yml_file),
            "--materialized",
            "view",
            "--manifest",
            manifest_path_str,
        ],
    )
    assert result == 0
