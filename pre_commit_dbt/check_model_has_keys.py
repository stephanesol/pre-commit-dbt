import argparse
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence

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
    # convert to sets
    models_missing_keys = {}

    for model in models:
        missing_keys = []
        for key in target_keys:
            if model.get(key) is None:
                missing_keys.append(key)
        if missing_keys:
            models_missing_keys[model.filename] = missing_keys


    for model, missing_keys in models_missing_keys.items():
        status_code = 1
        result = "\n- ".join(list(missing_keys))  # pragma: no mutate
        print(
            f"{sqls.get(model)}: "
            f"does not have some of the keys defined:\n- {result}",
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
