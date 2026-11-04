# LagaPy architecture

> **Design proposal, not an implementation inventory.** This document expands
> the original `Architecture.md` and preserves the roles of its initial
> `Lag*` classes. Implemented modules now include `src/lagapy/logging.py` and
> `src/lagapy/solver/`. Everything else remains a design proposal.

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
| `solver/` | **Implemented:** external CLI runner, Windows batch generation; future: solver settings and result/convergence checking |
| `results/` | In-memory results, queries, field histories, derived quantities |
| `visualization/` | Mesh, field, contour, history and convergence plotting |
| `logging.py` | **Implemented:** opt-in console/rotating-file logging with independent levels for the `lagapy` logger |
| `utils/` | Future small reusable functions without domain-specific responsibilities |

Except for `solver/`, these package names are **future boundaries**, not
empty Python packages.

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
results = LagamineResults.from_files("run_01")
fields = results.read_fields()
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

Execution is a separate, **implemented** service: `LagamineRunner` in
`lagapy.solver` uses `subprocess.run` with argument lists (no shell), explicit
`cwd`, configurable executable paths, optional capture of text output and
per-stage timeouts. It propagates execution errors and verifies only selected
inputs. Windows batch generation is available as a separate method. No solver process starts on import. **Not yet implemented:** solver
convergence checks, output-file readers, progress monitoring, and
Lagamine-specific integration tests. See [Execution](EXECUTION.md).

## Post-processing and visualisation

Results should be represented independently from Matplotlib or a particular
data-frame library. Readers convert output to typed, queryable results;
visualisation functions consume those results. Large meshes/results may
later require lazy loading or optional numerical dependencies.
