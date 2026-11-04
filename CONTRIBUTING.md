# Contributing to LagaPy

LagaPy is an early-stage research-software project. Contributions are welcome,
particularly verified Lagamine file-format examples, tests, and focused parsers.

## Before implementing a feature

- Read [Architecture](docs/ARCHITECTURE.md) and
  [File formats](docs/FILE_FORMATS.md).
- For a new format reader or writer, document the expected syntax and
  version/variant first; avoid guessing undocumented parts of the format.
- Avoid committing proprietary Lagamine binaries, confidential models, or
  research data without explicit permission.

## Development process

Create a Python 3.15 environment and install `requirements-dev.txt`.
Run tests, linting, formatting, type checks, and a package build:

```bash
python -m pytest
ruff check .
ruff format --check .
mypy
python -m build
```

New functionality should include unit tests. File I/O deserves fixture-based
golden-file tests and read-write-read tests whenever the file format permits.
Tests requiring Lagamine itself must be marked `@pytest.mark.lagamine` and
must not run implicitly in CI.

## Style and public APIs

Follow PEP 8: `snake_case` for modules/functions/variables, `PascalCase` for
classes, and `UPPER_SNAKE_CASE` for constants. Use `pathlib.Path`, type hints,
precise exceptions, docstrings, and consistent SI units where appropriate.
Keep parsing, model representation, subprocess execution, and plotting in
separate modules. Do not introduce public classes whose behaviour is still
undefined: a small tested interface is preferable to a broad placeholder API.

## Review and versioning

Record meaningful user-facing changes in `CHANGELOG.md`. Document format
limitations and solver-version assumptions. For substantial API changes,
discuss the design before implementing it.
