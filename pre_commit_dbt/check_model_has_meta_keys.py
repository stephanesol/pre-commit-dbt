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

    # get manifest nodes that pre-commit found as changed
    models = get_models(manifest, filenames)
    # if user added schema but did not rerun the model
    schemas = get_model_schemas(list(ymls.values()), filenames)

    # convert to sets
    model_key_dict = {}

    in_models = set()
    for model in models:
        keys = set(model.node.get("meta", {}).keys())
        model_key_dict[model.filename] = keys
        if set(meta_keys).issubset(keys):
            in_models.add(model.filename)

    in_schemas = set()
    for schema in schemas:
        keys = set(schema.schema.get("meta", {}).keys())
        if model_key_dict.get(schema.model_name, None):
            model_key_dict[schema.model_name].update({'keys': model_key_dict[schema.model_name].update(keys)})
        else:
            model_key_dict[schema.model_name] = keys

        if set(meta_keys).issubset(keys):
            in_schemas.add(schema.model_name)

    missing = filenames.difference(in_models, in_schemas)

    for model in missing:
        if model_key_dict.get(model,{}):
            status_code = 1
            model_keys = model_key_dict.get(model,set())
            missing_keys = set(meta_keys).difference(model_keys) if model_keys else meta_keys
            result = "\n- ".join(list(missing_keys))  # pragma: no mutate
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
