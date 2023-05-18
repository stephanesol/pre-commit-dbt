import argparse
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import add_manifest_args
from pre_commit_dbt.utils import get_filenames
from pre_commit_dbt.utils import get_json
from pre_commit_dbt.utils import get_model_schemas
from pre_commit_dbt.utils import get_model_sqls
from pre_commit_dbt.utils import get_models
from pre_commit_dbt.utils import get_disabled_models
from pre_commit_dbt.utils import JsonOpenError


def has_meta_key(
    paths: Sequence[str], manifest: Dict[str, Any], meta_key: str, meta_key_values: Sequence[str]
) -> int:
    status_code = 0
    ymls = get_filenames(paths, [".yml", ".yaml"])
    sqls = get_model_sqls(paths, manifest)
    filenames = set(sqls.keys())

    # get manifest nodes that pre-commit found as changed
    models = get_models(manifest, filenames)

    disabled_models = get_disabled_models(manifest, filenames)

    # if user added schema but did not rerun the model
    schemas = get_model_schemas(list(ymls.values()), filenames)

    # convert to sets
    model_key_value_dict = {}

    in_models = set()
    for model in models:
        key_value = model.node.get("meta", {}).get(meta_key, {})
        model_key_value_dict[model.filename] = key_value
        if set(key_value).issubset(meta_key_values):
            in_models.add(model.filename)

    in_disabled = set()
    for model in disabled_models:
        in_disabled.add(model.filename)

    in_schemas = set()
    for schema in schemas:
        key_value = set(schema.schema.get("meta", {}).get(meta_key, {}))
        model_key_value_dict[schema.model_name] = key_value

        if set(key_value).issubset(meta_key_values):
            in_schemas.add(schema.model_name)

    missing = filenames.difference(in_models, in_schemas, in_disabled)

    for model in missing:
        status_code = 1
        model_keys = model_key_value_dict.get(model,set())
        missing_keys = set(meta_key_values).difference(model_keys) if model_keys else meta_key_values
        result = "\n- ".join(list(missing_keys))  # pragma: no mutate
        print(
            f"{sqls.get(model)}: "
            f"value: {key_value} for key: {meta_key} is not valid:\n-",
            f"must be one of {meta_key_values}",
        )
    return status_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)
    add_manifest_args(parser)

    parser.add_argument(
        "--meta-key",
        type=str,
        required=True,
        help="Key to Check for Values",
    )

    parser.add_argument(
        "--meta-key-values",
        nargs="+",
        required=True,
        help="List of required values in meta part of model for a target key.",
    )

    args = parser.parse_args(argv)

    try:
        manifest = get_json(args.manifest)
    except JsonOpenError as e:
        print(f"Unable to load manifest file ({e})")
        return 1

    return has_meta_key(
        paths=args.filenames, manifest=manifest, meta_key=args.meta_key, meta_key_values=args.meta_key_values
    )


if __name__ == "__main__":
    exit(main())
