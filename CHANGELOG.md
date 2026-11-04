# Changelog

This project follows the principles of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and [Semantic Versioning](https://semver.org/). The software is in early
development; the version below is a **development snapshot**, not a claim of
a working Lagamine integration.

## [Unreleased]

### Added
- Standard-library-only `LagamineRunner` for Prepro and Lagamine execution,
  with per-stage input checks, working directory, optional timeout/output
  capture, and error propagation.
- Safe-by-default Windows batch generation and optional, lazily imported
  Windows dialog automation for graphical versions of Prepro.
- Dedicated opt-in `lagapy` logging with console/rotating-file handlers.
- Usage documentation, an executable workflow example, and targeted tests.

### Changed
- Archived supplied execution and logging prototypes in
  `legacy/execution_original/` instead of importing them into the package.


### Planned

- Typed FE domain objects for meshes, laws, conditions and solver settings.
- Readers and writers for verified Lagamine input formats.
- Result readers, data extraction and plotting.

## [0.1.0.dev0] - 2026-11-04

### Added

- Importable `src/lagapy` package stub and initial smoke test.
- Updated project metadata, citation, documentation, and development tools.
- Architecture and file-format inventory for incremental development.
- Original July 2026 class prototypes preserved unchanged in `legacy/`.

### Changed

- Replaced an unrelated balance-measurement README with LagaPy documentation.
- Corrected package discovery and reconciled the licence as GPL-3.0-or-later.
- Set the declared minimum Python version to 3.15.

### Notes

- Source files provided for this initial reconstruction contained an incomplete
  `0.1.0` changelog and inconsistent `0.3.0` metadata. This snapshot is
  deliberately labelled `0.1.0.dev0` until a release history is confirmed.
