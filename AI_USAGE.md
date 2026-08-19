# AI usage guide

This guide gives coding agents the shortest reliable path to understand and change `class-roster-simulator`.

## Package contract

The public API is exported from `class_roster`:

- `simulate_class(...) -> ClassRoster` generates a roster.
- `normalize_birth_range(...)` validates and expands an optional inclusive range.
- `Student` stores one fictional student's data and computes age on a date.
- `ClassRoster` stores one simulation result and renders terminal text.

The package does not impose a grade or school-year rule. When a birth range is used, both endpoints are required. Supported inputs are `datetime.date`, `YYYY`, `YYYY-MM`, and `YYYY-MM-DD`.

`src/class_roster/py.typed` marks the installed distribution as fully inline typed under PEP 561. Preserve annotations on all public APIs and do not remove the marker from built wheels.

## Repository map

```text
src/class_roster/       package code and py.typed marker
examples/               directly runnable starter programs
tests/                  behavior and distribution-contract tests
README.md               user-facing installation and usage
pyproject.toml          build metadata and CLI entry point
```

`alt_generate_zh_name` is a pinned Git dependency. Its `generate()` function returns a pandas `DataFrame` with the columns `姓名`, `性别`, and `生日`.

## Development rules

1. Keep `birth_start` and `birth_end` semantics synchronized across the Python API, CLI, README, and examples.
2. Add an `Example:` section with executable `>>>` snippets to every function and method docstring, including internal helpers.
3. Keep generated data explicitly fictional and avoid adding real personal data to fixtures or examples.
4. Add or update tests for behavior changes.
5. Keep `llms.txt`, this guide, examples, and `py.typed` in source distributions; keep `py.typed` in wheels.

## Validation

From the repository root in PowerShell:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -o addopts='' -q -p no:cacheprovider
.\.venv\Scripts\python.exe examples\basic_roster.py
.\.venv\Scripts\python.exe -m build --no-isolation
```

After building, inspect both archives and run the example against an installed wheel before treating a release as verified.
