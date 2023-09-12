import argparse
from typing import Any, Dict, Optional, Sequence

from pre_commit_dbt.utils import (JsonOpenError, add_filenames_args,
                                  add_manifest_args, get_json, get_model_sqls,
                                  get_models)


def validate_incremental_models(
    paths: Sequence[str], manifest: Dict[str, Any], materialized: Sequence[str]
) -> int:
    status_code = 0
    sqls = get_model_sqls(paths, manifest)
    filenames = set(sqls.keys())

    # get manifest nodes that pre-commit found as changed
    models = get_models(manifest, filenames)
    for model in models:
        model_materialized = set([model.node.get("config", {}).get("materialized", None)])
        if model_materialized == set(["incremental"]):
            # check if the sql contains a list of terms
            # if it does, then it is a backfill model
            # if it does not, then it is a regular incremental model
            if "select" in model.sql.lower():
                status_code = 1
                print(
                    f"{model.node.get('original_file_path', model.filename)}: "
                    f"has invalid materialized:\n- {result}",
                )


        if not model_materialized.issubset(valid_materialized):
            status_code = 1
            list_diff = list(model_materialized.difference(valid_materialized))
            result = "\n- ".join(filter(None, list_diff))  # pragma: no mutate
            print(
                f"{model.node.get('original_file_path', model.filename)}: "
                f"has invalid materialized:\n- {result}",
            )
    return status_code


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)
    add_manifest_args(parser)

    parser.add_argument(
        "--materialized",
        nargs="+",
        required=True,
        help="A list of materializations that models can have.",
    )

    args = parser.parse_args(argv)

    try:
        manifest = get_json(args.manifest)
    except JsonOpenError as e:
        print(f"Unable to load manifest file ({e})")
        return 1

    return validate_materialization(paths=args.filenames, manifest=manifest, materialized=args.materialized)


if __name__ == "__main__":
    exit(main())
