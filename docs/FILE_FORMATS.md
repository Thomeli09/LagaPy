# Lagamine file-format inventory

This inventory captures the original notes and class docstrings. **No format
specification, reference file, parser or writer was supplied in this ZIP.**
Roles are provisional until verified against real, shareable Lagamine files.

| Extension | Intended use from the prototype | Validation needed |
|---|---|---|
| `.lag` | Main model description; includes mesh and possibly material/condition data | Sections, record syntax, units, ordering, variant differences |
| `.dat` | Solver/analysis configuration (`LagSolver`) | Fields, settings, execution arguments |
| `.pri` | Data printing / requested output information (`LagPri`) | Relationship to output results and print controls |
| `.dep` | Initial/boundary conditions, and potentially extracted data in some workflows | Confirm whether input, output, or both; actual sections |
| `.ipn` | Results to read and inspect | Nodal/integration-point role, array layout, indexing |
| `.ipe` | Results to read and inspect | Nodal/integration-point role, array layout, indexing |
| Other diagnostic/log files | Error diagnostics and solver execution reports | Extensions, encoding, error semantics |

The `.dep`, `.ipn`, and `.ipe` descriptions are deliberately not more
specific: guessing their internal meaning would make future readers unsafe.

## Information to gather for each file family

1. One minimal valid sample and one realistic, nonconfidential sample.
2. Lagamine executable version / module producing or consuming the file.
3. Whether the file is input, output, or bidirectional.
4. Encoding, line endings, decimal conventions, precision and delimiters.
5. Section syntax, IDs, numbering conventions and cross-file references.
6. Rules for optional records, nested blocks, continuation lines and comments.
7. Expected parsed model/results and negative cases for diagnostics.

A successful reader is not sufficient: the initial milestone should verify
**read → write → read** equivalence for supported data and check a solver run
separately when a usable Lagamine executable is available.
