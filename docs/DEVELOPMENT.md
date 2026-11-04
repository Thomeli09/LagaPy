# Development guide

## Python environment

Python **3.15** is the supported target; no runtime features rely on a solver
executable yet. Create a dedicated virtual environment per checkout.

```powershell
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

For Linux/macOS substitute `python3.15 -m venv .venv` and
`source .venv/bin/activate`.

## Checks

```bash
python -m pytest -q
ruff check .
ruff format --check .
mypy
python -m build
```

The tests include logging and runner unit tests and a small **synthetic**
executable workflow test. They do not establish correctness with a real
Lagamine executable or validate FEM convergence; such tests must be opt-in.

## Coding style

- Use PEP 8 names, type annotations, `pathlib.Path` and meaningful exceptions.
- Prefer data-oriented/composable objects over deep class inheritance.
- Keep functions focused on one responsibility; avoid module-level side effects.
- Distinguish modelling objects from file formats and process management.
- Document units, coordinate systems, indexing and solver versions explicitly.
- Write tests for format round-trips, parse failures and numerical invariants.
- Let tests that need Lagamine be opt-in and independent of unit tests.

## Project metadata

The version is set in `pyproject.toml` and mirrored in `CITATION.cff`
when releasing. The importable package obtains the installed version via
`importlib.metadata`; a checkout not installed returns `0+unknown`.
Runtime and extra dependency declarations in `pyproject.toml` are canonical;
`requirements*.txt` are convenience editable-install wrappers.

## Scope and licences

Lagamine is an external solver: the presence of a local executable does not
imply permission to redistribute it. Do not add the binary to the repository.
Consult the applicable solver licence and institutional requirements.
