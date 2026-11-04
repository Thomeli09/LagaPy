# LagaPy architecture

> **Design proposal, not an implementation inventory.** This document expands
> the original `Architecture.md` and preserves the roles of its initial
> `Lag*` classes. The only implemented package module at present is
> `src/lagapy/__init__.py`.

## Responsibilities

```text
                Application scripts / examples
                           |
                 High-level project API
                           |
         +-----------------+------------------+
         |                                    |
   FE domain model                       Workflow service
   mesh / laws /                         solver execution
   conditions / steps                         |
         |                                    |
         +---------+--------------------------+
                   |
              I/O adapters
    .lag / .dat / .pri / .dep / .ipn / .ipe
                   |
             Files on disk
                   |
         External Lagamine binary
                   |
          Results / post-processing
                   |
               Visualisation
```

Domain objects should not depend on file paths or a concrete parser. A mesh
built in memory should be reusable by writers, validators and plotting
functions. File paths belong to I/O and workflow layers.

## Proposed `src/lagapy/` modules

| Package | Responsibility |
|---|---|
| `core/` | Project/model aggregation, metadata, validation, shared exceptions |
| `mesh/` | Nodes, elements, groups, geometry, mesh transforms |
| `materials/` | Material properties and constitutive law definitions |
| `conditions/` | Initial conditions, boundary conditions, time-dependent loads |
| `analysis/` | Problem definition, analysis steps, field/output requests |
| `io/` | Readers/writers, tokenisation, version- and format-specific adapters |
| `solver/` | Solver configuration, executable runner, return codes, logs |
| `results/` | In-memory results, queries, field histories, derived quantities |
| `visualization/` | Mesh, field, contour, history and convergence plotting |
| `utils/` | Small reusable functions without domain-specific responsibilities |

These directories are **future boundaries**, not empty Python packages.

## Relationship to the original classes

| Original prototype | Proposed future role |
|---|---|
| `Lagamine` (`Python2Lagamine.py`) | High-level simulation/project coordinator |
| `LagGeneric` | Shared metadata/value-object conventions, only if useful |
| `LagMesh` | Explicit mesh objects and compatible input/output adapters |
| `LagLaw` | Constitutive law description and serialization |
| `LagCond` | Initial/boundary conditions and compatible file sections |
| `LagSolver` | Solver control settings, distinct from subprocess execution |
| `LagPri` | Output/print requests and their file representation |

Do not automatically reproduce the old inheritance structure. The original
`getName` properties and path handling are incomplete; the new API should
prefer descriptive Python attributes such as `name: str` and `path: Path`,
composition, validation, and explicit `read_*`/`write_*` operations.

## Proposed APIs (illustrative only)

```python
# Design sketch — NOT IMPLEMENTED. Do not copy into runnable examples yet.
model = LagamineProject.from_files("case.lag", "case.dat")
model.mesh.validate()
model.write_inputs("run_01")
result = LagamineRunner(executable="/path/to/lagamine").run("run_01")
fields = result.read_fields()
```

The eventual public API must be designed from actual working format examples
and tested class responsibilities; names in this sketch are not committed API.

## Parsing and writing contract

- Readers accept `Path` and should distinguish unsupported sections from
  malformed sections with informative errors and file/line context.
- Writers should be deterministic, encoding- and locale-aware, and preserve
  numeric precision relevant to Lagamine.
- Preserve unrecognised format blocks where practical; otherwise reject
  round trips that would silently discard essential information.
- Do not conflate file extensions with unique schemas until verified: input
  and output roles may depend on the workflow or Lagamine release.
- Keep original sample files in fixtures to test round trips and expected
  numerical values, with the right to redistribute them confirmed.

## Solver execution contract

Execution is a separate, optional service that will use `subprocess` with a
list of arguments (`shell=False`), explicit working directory and configurable
executable path. Capture return codes and diagnostic output. A timeout,
executable not found, or failed simulation should raise an actionable error.
No solver process should be triggered by importing `lagapy`.

## Post-processing and visualisation

Results should be represented independently from Matplotlib or a particular
data-frame library. Readers convert output to typed, queryable results;
visualisation functions consume those results. Large meshes/results may
later require lazy loading or optional numerical dependencies.
