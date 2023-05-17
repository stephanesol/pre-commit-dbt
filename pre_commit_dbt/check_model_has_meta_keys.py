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
from pre_commit_dbt.utils import JsonOpenError


def has_meta_key(
    paths: Sequence[str], manifest: Dict[str, Any], meta_keys: Sequence[str]
) -> int:
    status_code = 0
    ymls = get_filenames(paths, [".yml", ".yaml"])
    sqls = get_model_sqls(paths, manifest)
    filenames = set(sqls.keys())

    print(f"target keys : {meta_keys}")
    print(f"filenames : {filenames}")
    # get manifest nodes that pre-commit found as changed
    models = get_models(manifest, filenames)
    # if user added schema but did not rerun the model
    schemas = get_model_schemas(list(ymls.values()), filenames)

    print(f"schemas : {schemas}")
    # convert to sets
    in_models = set()
    for model in models:
        keys = set(model.node.get("meta", {}).keys())
        print(keys)
        if set(meta_keys).issubset(keys):
            in_models.add(model.filename)

    print(f"in_models: {in_models}")

    in_schemas = set()
    for schema in schemas:
        keys = set(schema.schema.get("meta", {}).keys())
        print(keys)
        if set(meta_keys).issubset(keys):
            in_schemas.add(schema.model_name)

    print(f"in_schemas: {in_schemas}")

    missing = filenames.difference(in_models, in_schemas)

    print(missing)

    for model in missing:
        status_code = 1
        result = "\n- ".join(list(meta_keys))  # pragma: no mutate
        print(
            f"{sqls.get(model)}: "
            f"does not have some of the meta keys defined:\n- {result}",
        )
    return status_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)
    add_manifest_args(parser)

    parser.add_argument(
        "--meta-keys",
        nargs="+",
        required=True,
        help="List of required key in meta part of model.",
    )

    args = parser.parse_args(argv)

    try:
        manifest = get_json(args.manifest)
    except JsonOpenError as e:
        print(f"Unable to load manifest file ({e})")
        return 1

    return has_meta_key(
        paths=args.filenames, manifest=manifest, meta_keys=args.meta_keys
    )


if __name__ == "__main__":
    exit(main())
