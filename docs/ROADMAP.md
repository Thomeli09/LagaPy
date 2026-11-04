# Roadmap

This roadmap is ordered by implementation dependencies, not a promise of
delivery dates. Items are **planned** unless checked off.

## Phase 0 — Repository foundation

- [x] Preserve the provided prototype source in `legacy/`.
- [x] Establish packaging, metadata, documentation and Python 3.15 target.
- [x] Provide a minimal importable package and smoke tests.
- [ ] Validate an install, build and tests on Python **3.15**.

## Phase 1 — Verified file representation

- [ ] Obtain suitable, redistributable example `.lag`, `.dat`, `.pri` and result files.
- [ ] Document one exact version of each format rather than generalising early.
- [ ] Implement a minimal `Mesh` / element / node representation.
- [ ] Add strict read/write support for a limited `.lag` subset and round-trip tests.
- [ ] Model constitutive law definitions and initial/boundary conditions as needed.

## Phase 2 — Analysis assembly and execution

- [ ] Generate mutually consistent input files from a single Python project object.
- [ ] Implement a configurable external Lagamine runner with logs and robust errors.
- [ ] Add opt-in end-to-end integration tests for a simple validated model.

## Phase 3 — Results and visualisation

- [ ] Read `.ipn`, `.ipe`, `.dep` and diagnostic files as their formats become known.
- [ ] Provide field/time-history selection and derived numerical results.
- [ ] Add plotting of meshes, fields, contours, deformations and histories.

## Phase 4 — Extensibility and usability

- [ ] Document 2D/3D and specialised analysis workflows.
- [ ] Add example cases for geotechnics and metal forming where licensing permits.
- [ ] Expand validation, logging, CLI, interoperable mesh formats and documentation.

A useful first implementation task is to contribute one valid sample `.lag`
file together with the matching expected nodes, elements and material records.
