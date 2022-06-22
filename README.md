<p align="center">
 <img src=".github/pre-commit-dbt.png" alt="dbt-pre-commit" width=600/>
 <h1 align="center">pre-commit-dbt</h1>
</p>
<p align="center">
 <a href="https://github.com/offbi/pre-commit-dbt/actions?workflow=CI">
 <img src="https://github.com/offbi/pre-commit-dbt/workflows/CI/badge.svg?branch=main" alt="CI" />
 </a>
 <a href="https://codecov.io/gh/offbi/pre-commit-dbt">
 <img src="https://codecov.io/gh/offbi/pre-commit-dbt/branch/main/graph/badge.svg"/>
 </a>
 <a href="https://github.com/psf/black">
 <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="black"/>
 </a>
 <a href="https://github.com/pre-commit/pre-commit">
 <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white" alt="black"/>
 </a>
</p>

List of [pre-commit](https://pre-commit.com) hooks to ensure the quality of your [dbt](https://www.getdbt.com) projects.

## Goal

*Quick ensure the quality of your `dbt` projects*.

`dbt` is awesome, but when a number of models, sources, and macros grow it starts to be challenging to maintain quality. People often forget to update columns in schema files, add descriptions, or test. Besides, with the growing number of objects, dbt slows down, users stop running models/tests (because they want to deploy the feature quickly), and the demands on reviews increase.

If this is the case, `pre-commit-dbt` is here to help you!

## List of `pre-commit-dbt` hooks

:bulb: Click on hook name to view the details.

**Model checks:**
 * [`check-column-desc-are-same`](HOOKS.md#check-column-desc-are-same): Check column descriptions are the same.
 * [`check-column-name-contract`](HOOKS.md#check-column-name-contract): Check column name abides to contract.
 * [`check-model-columns-have-desc`](HOOKS.md#check-model-columns-have-desc): Check the model columns have description.
 * [`check-model-has-all-columns`](HOOKS.md#check-model-has-all-columns): Check the model has all columns in the properties file.
 * [`check-model-has-description`](HOOKS.md#check-model-has-description): Check the model has description.
 * [`check-model-has-meta-keys`](HOOKS.md#check-model-has-meta-keys): Check the model has keys in the meta part.
 * [`check-model-has-keys`](HOOKS.md#check-model-has-keys): Check the model has the specified keys.
 * [`check-model-has-properties-file`](HOOKS.md#check-model-has-properties-file): Check the model has properties file.
 * [`check-model-has-tests-by-name`](HOOKS.md#check-model-has-tests-by-name): Check the model has a number of tests by test name.
 * [`check-model-has-tests-by-type`](HOOKS.md#check-model-has-tests-by-type): Check the model has a number of tests by test type.
 * [`check-model-has-tests-by-group`](HOOKS.md#check-model-has-tests-by-group): Check the model has a number of tests from a group of tests.
 * [`check-model-has-tests`](HOOKS.md#check-model-has-tests): Check the model has a number of tests.
 * [`check-model-name-contract`](HOOKS.md#check-model-name-contract): Check model name abides to contract.
 * [`check-model-parents-and-childs`](HOOKS.md#check-model-parents-and-childs): Check the model has a specific number (max/min) of parents or/and childs.
 * [`check-model-parents-database`](HOOKS.md#check-model-parents-database): Check the parent model has a specific database.
 * [`check-model-parents-schema`](HOOKS.md#check-model-parents-schema): Check the parent model has a specific schema.
 * [`check-model-tags`](HOOKS.md#check-model-tags): Check the model has valid tags.
 * [`check-model-materialized`](HOOKS.md#check-model-materialized): Check the model has valid materialization option.

**Script checks:**
 * [`check-script-semicolon`](HOOKS.md#check-script-semicolon): Check the script does not contain a semicolon.
 * [`check-script-has-no-table-name`](HOOKS.md#check-script-has-no-table-name): Check the script has not table name (is not using `source()` or `ref()` macro for all tables).
 * [`check-script-ref-and-source`](HOOKS.md#check-script-ref-and-source): Check the script has only existing refs and sources.

**Source checks:**
 * [`check-source-columns-have-desc`](HOOKS.md#check-source-columns-have-desc): Check for source column descriptions.
 * [`check-source-has-all-columns`](HOOKS.md#check-source-has-all-columns): Check the source has all columns in the properties file.
 * [`check-source-table-has-description`](HOOKS.md#check-source-table-has-description): Check the source table has description.
 * [`check-source-has-freshness`](HOOKS.md#check-source-has-freshness): Check the source has the freshness.
 * [`check-source-has-loader`](HOOKS.md#check-source-has-loader): Check the source has loader option.
 * [`check-source-has-meta-keys`](HOOKS.md#check-source-has-meta-keys): Check the source has keys in the meta part.
 * [`check-source-has-tests-by-name`](HOOKS.md#check-source-has-tests-by-name): Check the source has a number of tests by test name.
 * [`check-source-has-tests-by-type`](HOOKS.md#check-source-has-tests-by-type): Check the source has a number of tests by test type.
 * [`check-source-has-tests`](HOOKS.md#check-source-has-tests): Check the source has a number of tests.
 * [`check-source-tags`](HOOKS.md#check-source-tags): Check the source has valid tags.
 * [`check-source-childs`](HOOKS.md#check-source-childs): Check the source has a specific number (max/min) of childs.

**Macro checks:**
 * [`check-macro-has-description`](HOOKS.md#check-macro-has-description): Check the macro has description.
 * [`check-macro-arguments-have-desc`](HOOKS.md#check-macro-arguments-have-desc): Check the macro arguments have description.

**Modifiers:**
 * [`generate-missing-sources`](HOOKS.md#generate-missing-sources): If any source is missing this hook tries to create it.
 * [`generate-model-properties-file`](HOOKS.md#generate-model-properties-file): Generate model properties file.
 * [`unify-column-description`](HOOKS.md#unify-column-description): Unify column descriptions across all models.
 * [`replace-script-table-names`](HOOKS.md#replace-script-table-names): Replace table names with `source()` or `ref()` macros in the script.
 * [`remove-script-semicolon`](HOOKS.md#remove-script-semicolon): Remove the semicolon at the end of the script.

**dbt commands:**
 * [`dbt-clean`](HOOKS.md#dbt-clean): Run `dbt clean` command.
 * [`dbt-compile`](HOOKS.md#dbt-compile): Run `dbt compile` command.
 * [`dbt-deps`](HOOKS.md#dbt-deps): Run `dbt deps` command.
 * [`dbt-docs-generate`](HOOKS.md#dbt-docs-generate): Run `dbt docs generate` command.
 * [`dbt-run`](HOOKS.md#dbt-run): Run `dbt run` command.
 * [`dbt-test`](HOOKS.md#dbt-test): Run `dbt test` command.

---
:exclamation:**If you have an idea for a new hook or you found a bug, [let us know](https://github.com/offbi/pre-commit-dbt/issues/new)**:exclamation:
## Install

For detailed installation and usage, instructions see [pre-commit.com](https://pre-commit.com) site.

```
pip install pre-commit
```
## Setup

1. Create a file named `.pre-commit-config.yaml` in your `dbt` root folder.
2. Add [list of hooks](#list-of-pre-commit-dbt-hooks) you want to run befor every commit. E.g.:
```
repos:
- repo: https://github.com/offbi/pre-commit-dbt
  rev: v1.0.0
  hooks:
  - id: check-script-semicolon
  - id: check-script-has-no-table-name
  - id: dbt-test
  - id: dbt-docs-generate
  - id: check-model-has-all-columns
    name: Check columns - core
    files: ^models/core
  - id: check-model-has-all-columns
    name: Check columns - mart
    files: ^models/mart
  - id: check-model-columns-have-desc
    files: ^models/mart
```
3. Optionally, run `pre-commit install` to set up the git hook scripts. With this, `pre-commit` will run automatically on `git commit`! You can also manually run `pre-commit run` after you `stage` all files you want to run. Or `pre-commit run --all-files` to run the hooks against all of the files (not only `staged`).

## Run as Github Action

Unfortunately, you cannot natively use `pre-commit-dbt` if you are using **dbt Cloud**. But you can run checks after you push changes into Github.

`pre-commit-dbt` for the most of the hooks needs `manifest.json` (see requirements section in hook documentation), that is in the `target` folder. Since this target folder is usually in `.gitignore`, you need to generate it. For that you need to run `dbt-compile` (or `dbt-run`) command.
To be able to compile dbt, you also need [profiles.yml](https://docs.getdbt.com/dbt-cli/configure-your-profile) file with your credentials. **To provide passwords and secrets use Github Secrets** (see example).

So you want to e.g. run chach on number of tests:

```
repos:
- repo: https://github.com/offbi/pre-commit-dbt
 rev: v1.0.0
 hooks:
 - id: check-model-has-tests
   args: ["--test-cnt", "2", "--"]
```

To be able to run this in Github actions you need to modified it to:

```
repos:
- repo: https://github.com/offbi/pre-commit-dbt
 rev: v1.0.0
 hooks:
 - id: dbt-compile
   args: ["--cmd-flags", "++profiles-dir", "."]
 - id: check-model-has-tests
   args: ["--test-cnt", "2", "--"]
```

### Create profiles.yml

First step is to create [profiles.yml](https://docs.getdbt.com/dbt-cli/configure-your-profile). E.g.

```
# example profiles.yml file
jaffle_shop:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      user: alice
      password: "{{ env_var('DB_PASSWORD') }}"
      port: 5432
      dbname: jaffle_shop
      schema: dbt_alice
      threads: 4
```

and store this file in project root `./profiles.yml`.


### Create new workflow

- inside your Github repository create folder `.github/workflows` (unless it already exists).
- create new file e.g. `main.yml`
- specify your workflow e.g.:


```
name: pre-commit

on:
  pull_request:
  push:
  branches: [main]

jobs:
  pre-commit:
  runs-on: ubuntu-latest
  steps:
  - uses: actions/checkout@v2
  - uses: actions/setup-python@v2
  - id: file_changes
    uses: trilom/file-changes-action@v1.2.4
    with:
      output: ' '
  - uses: offbi/pre-commit-dbt@v1.0.0
    env:
      DB_PASSWORD: ${{ secrets.SuperSecret }}
    with:
      args: run --files ${{ steps.file_changes.outputs.files}}
```
