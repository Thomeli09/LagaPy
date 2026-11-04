"""Smoke tests for the initial installable package."""

import lagapy


def test_import_exposes_a_version_string() -> None:
    assert isinstance(lagapy.__version__, str)
    assert bool(lagapy.__version__)


def test_no_unimplemented_solver_api_is_exported() -> None:
    assert lagapy.__all__ == ["__version__"]
