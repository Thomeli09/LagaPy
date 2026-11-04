"""Unit tests for separate console/file logging levels and handler lifecycle."""

import logging
from logging.handlers import RotatingFileHandler

import pytest

from lagapy.logging import configure_logging


@pytest.fixture(autouse=True)
def restore_logger():
    logger = logging.getLogger("lagapy")
    handlers = logger.handlers[:]
    level = logger.level
    propagate = logger.propagate
    yield
    for handler in logger.handlers[:]:
        if handler not in handlers:
            logger.removeHandler(handler)
            handler.close()
    for handler in handlers:
        if handler not in logger.handlers:
            logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = propagate


def test_does_not_change_root_logger(tmp_path) -> None:
    root = logging.getLogger()
    before = root.handlers[:], root.level
    configure_logging(output=tmp_path / "run.log")
    assert (root.handlers, root.level) == before


def test_different_levels_for_console_and_file(tmp_path, capsys) -> None:
    path = tmp_path / "logs" / "case.log"
    logger = configure_logging(
        output=path,
        console_level=logging.WARNING,
        file_level=logging.DEBUG,
    )
    assert logger.level == logging.DEBUG
    assert logger.propagate is False
    assert [handler.level for handler in logger.handlers] == [logging.WARNING, logging.DEBUG]

    # Messages emitted by any child module must pass through the same handlers.
    child = logging.getLogger("lagapy.solver.runner")
    child.debug("diagnostic")
    child.info("case started")
    child.warning("potential issue")

    console = capsys.readouterr().err
    assert "potential issue" in console
    assert "diagnostic" not in console
    assert "case started" not in console
    text = path.read_text(encoding="utf-8")
    assert "diagnostic" in text
    assert "case started" in text
    assert "potential issue" in text


def test_console_only(tmp_path, capsys) -> None:
    logger = configure_logging(console_level=logging.INFO)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    logger.info("console works")
    assert "console works" in capsys.readouterr().err


def test_file_only(tmp_path, capsys) -> None:
    target = tmp_path / "file_only.log"
    logger = configure_logging(console_level=None, output=target)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], RotatingFileHandler)
    logger.debug("file works")
    assert not capsys.readouterr().err
    assert "file works" in target.read_text(encoding="utf-8")


def test_reconfiguration_does_not_duplicate_entries_and_appends(tmp_path) -> None:
    target = tmp_path / "case.log"
    logger = configure_logging(console_level=None, output=target)
    logger.info("first run")
    logger = configure_logging(console_level=None, output=target)
    logger.info("second run")
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], RotatingFileHandler)
    contents = target.read_text(encoding="utf-8")
    assert contents.count("first run") == 1
    assert contents.count("second run") == 1


def test_can_disable_both_outputs() -> None:
    logger = configure_logging(console_level=None)
    assert not logger.handlers
    assert logger.propagate is False


def test_notset_handler_does_not_inherit_root_filter(tmp_path) -> None:
    target = tmp_path / "all.log"
    logger = configure_logging(console_level=None, output=target, file_level=logging.NOTSET)
    assert logger.level == 1
    logger.debug("still writes debug")
    assert "still writes debug" in target.read_text(encoding="utf-8")


def test_rotation(tmp_path) -> None:
    target = tmp_path / "rotate.log"
    logger = configure_logging(
        console_level=None, output=target, max_bytes=120, backup_count=2
    )
    for index in range(20):
        logger.info("line %d", index)
    assert (tmp_path / "rotate.log.1").exists()


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_bytes": 0},
        {"backup_count": -1},
        {"console_level": -1},
        {"file_level": -1},
        {"console_level": True},
        {"file_level": None},
    ],
)
def test_invalid_settings(kwargs) -> None:
    with pytest.raises(ValueError):
        configure_logging(**kwargs)


def test_invalid_output_does_not_replace_existing_handlers(tmp_path) -> None:
    logger = configure_logging(console_level=None, output=tmp_path / "working.log")
    original_handlers = logger.handlers[:]
    directory = tmp_path / "directory"
    directory.mkdir()
    with pytest.raises(OSError):
        configure_logging(console_level=None, output=directory)
    assert logger.handlers == original_handlers
    logger.info("keeps working")
    assert "keeps working" in (tmp_path / "working.log").read_text(encoding="utf-8")
