import argparse
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence

import yaml

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import get_filenames
from pre_commit_dbt.utils import get_model_schemas
from pre_commit_dbt.utils import JsonOpenError


def has_key(
    paths: Sequence[str], keys: Sequence[str]
) -> int:
    target_keys = set(keys)
    status_code = 0
    filenames = get_filenames(paths, [".yml", ".yaml"])
    #get model schemas from yaml
    models = get_model_schemas(list(filenames.values()), filenames)

    models_missing_keys = {}

    for schema in schemas:
        schema_keys = set(schema.schema.keys())
        missing_keys = target_keys - schema_keys
        if missing_keys:
            models_missing_keys[schema.file] = missing_keys
            status_code = 1

    for model, missing_keys in models_missing_keys.items():
        print(
            f"{model} : missing keys : {', '.join(missing_keys)}"
        )

    return status_code

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)

    parser.add_argument(
        "--keys",
        nargs="+",
        required=True,
        help="List of required keys in the model.",
    )

    args = parser.parse_args(argv)

    return has_key(
        paths=args.filenames, keys=args.keys
    )


if __name__ == "__main__":
    exit(main())
