# LagaPy

**LagaPy** is an open-source Python interface for preparing, running, and analysing
finite element (FE) simulations with **Lagamine**, the solver developed at the
University of Liège (ULiège).

The long-term goal is to let users describe a simulation with Python objects,
import an existing Lagamine model, generate the required input files, launch an
**externally installed** Lagamine executable, then retrieve and visualise the
results. The intended applications include geotechnical engineering,
metal forming, and other FE problems supported by Lagamine.

> **Status — early development (`0.1.0.dev0`).** This repository is currently a
> packaging and documentation foundation, **not yet a working Lagamine interface**.
> The archived prototype classes are in [`legacy/`](legacy/); readers, writers,
> execution, and plotting described below are **planned**, not implemented.

## Goals

- **Work with existing models:** parse Lagamine input/output files into typed
  Python objects, preserving information needed for round-trip conversion.
- **Build models programmatically:** define meshes, material/constitutive laws,
  initial and boundary conditions, solver settings, and requested outputs.
- **Write valid solver inputs:** generate compatible files using dedicated,
  testable format-specific writers rather than assembling strings in user scripts.
- **Run simulations:** configure and invoke an existing Lagamine executable,
  managing working directories, subprocess errors, and run logs.
- **Analyse results:** load relevant output files, extract numerical quantities,
  and plot FE fields, histories, meshes, and other computed data.
- **Stay extensible:** support different analysis types and, where necessary,
  format versions and executable configurations without tying the data model to
  one file format.

## Intended workflow

```text
Existing Lagamine files        Python-defined FE model
           |                            |
           +------------+---------------+
                        |
                 Read / construct
                        |
                Python model objects
                        |
                Validate / modify
                        |
                 Write input files
                        |
             External Lagamine solver
                        |
                Read output files
                        |
              Analyse / visualise
```

The file formats mentioned in the original design notes include `.lag`, `.dat`,
`.pri`, `.dep`, `.ipn`, and `.ipe`. Their exact structure, relationships, and
variant-dependent semantics must be confirmed against representative Lagamine
files before parsers and writers are implemented. See
[File formats](docs/FILE_FORMATS.md).

## Project layout

```text
LagaPy/
├── README.md                   # Project overview and status
├── CITATION.cff                # Citation metadata
├── CHANGELOG.md                # Changes by release
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # GPL-3.0-or-later
├── pyproject.toml              # Packaging, dependencies, tools
├── requirements.txt            # Editable installation
├── requirements-dev.txt        # Development and plotting extras
├── src/
│   └── lagapy/
│       ├── __init__.py         # Importable package foundation
│       └── py.typed            # Marker for typed public interfaces
├── docs/
│   ├── ARCHITECTURE.md         # Proposed subsystem boundaries
│   ├── DEVELOPMENT.md          # Setup, tests, coding conventions
│   ├── FILE_FORMATS.md         # Formats to investigate
│   └── ROADMAP.md              # Implementation order
├── examples/README.md         # Future runnable examples
├── tests/                      # Initial smoke tests; future fixtures
└── legacy/                     # Original prototype classes, unchanged
```

The future modules (such as `mesh`, `materials`, `conditions`, `io`, `solver`,
`results`, and `visualization`) are documented in
[Architecture](docs/ARCHITECTURE.md). They have **not** been created as empty
public APIs: they will be introduced with tested implementations.

## Requirements and installation

- **Python 3.15 or newer** is the declared target. Python 3.15 was released in
  October 2026; compatibility with it still needs testing in the target environment.
- A local Lagamine executable and any required licences/configuration will be
  needed **later**, when execution support is added. The executable and Lagamine
  itself are **not shipped** or licensed as part of LagaPy.
- No third-party runtime libraries are currently required for the package stub.

On Windows PowerShell:

```powershell
git clone https://github.com/Thomeli09/lagapy.git
cd lagapy
py -3.15 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

On Linux/macOS:

```bash
python3.15 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

`requirements.txt` installs the project in editable mode (`-e .`), while
`requirements-dev.txt` installs `-e .[dev,plot]`. Dependency definitions live
in `pyproject.toml`; the `plot` extra is reserved for future plotting features.

### Check the package foundation

```bash
python -c "import lagapy; print(lagapy.__version__)"
python -m pytest
ruff check .
ruff format --check .
python -m build
```

**There is not yet a runnable FE simulation example or a CLI.** The first
functional milestone is reading and writing a single, well-documented Lagamine
format with fixture-based tests.

## Design principles

1. **Separate the FE model from its file representation.** Meshes, laws,
   conditions, and results should be usable without any particular file reader.
2. **Keep parsing and writing symmetrical.** Where feasible, use read-write-read
   round-trip tests and clearly report unsupported constructs.
3. **Make execution optional.** Users should be able to inspect or generate
   files without having Lagamine installed.
4. **Prefer explicit types and naming.** Public names will follow PEP 8, while
   mapping the original `LagMesh`, `LagLaw`, `LagCond`, `LagSolver`, and
   `LagPri` ideas to modern, focused objects.
5. **Keep numerical and plotting dependencies optional** until they are needed.

## Documentation and contributions

Begin with the [architecture](docs/ARCHITECTURE.md),
[file format inventory](docs/FILE_FORMATS.md), and
[roadmap](docs/ROADMAP.md). Developers should read
[development instructions](docs/DEVELOPMENT.md) and
[contribution guidelines](CONTRIBUTING.md).

To implement accurate readers and writers, the project will need *shareable,
representative* Lagamine input/output examples (including expected data and
their interpretation). Do not commit confidential simulation models or
proprietary solver binaries.

## Citation

If LagaPy is used in research, please cite the software using
[`CITATION.cff`](CITATION.cff). The provisional citation is:

```bibtex
@software{Thommes_LagaPy_2026,
  author  = {Thommes, Eliott},
  title   = {LagaPy: Python tools for Lagamine finite element workflows},
  year    = {2026},
  version = {0.1.0.dev0},
  url     = {https://github.com/Thomeli09/lagapy}
}
```

Author: **Eliott Thommes** · [ORCID 0009-0005-0697-2438](https://orcid.org/0009-0005-0697-2438).

## Licence and disclaimer

LagaPy is licensed under the **GNU General Public License, version 3 or later
(GPL-3.0-or-later)**. See [`LICENSE`](LICENSE). This licence applies to LagaPy;
it does **not** grant permission to redistribute or use the separate Lagamine
executable beyond its own terms.

LagaPy is provided *as-is*, without warranty. It is under development and
must be independently validated before relying on results in research,
engineering design, or safety-critical applications. The numerical solution
is produced by Lagamine, not by LagaPy itself.
