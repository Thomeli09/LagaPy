"""Tests for subprocess invocation, workdir, generated inputs and batch files."""

import os
import subprocess
from pathlib import Path

import pytest

from lagapy.solver import LagamineRunner


def _make_inputs(tmp_path: Path):
    directory = tmp_path / "a case with spaces"
    directory.mkdir()
    lag_file = directory / "sample.LAG"
    lag_file.write_text("example", encoding="utf-8")
    dat_file = directory / "sample.DAT"
    preprocessor = directory / "Prepro.exe"
    solver = directory / "Lagamine.exe"
    preprocessor.write_text("placeholder", encoding="utf-8")
    solver.write_text("placeholder", encoding="utf-8")
    runner = LagamineRunner(
        lag_file="sample.LAG",
        dat_file="sample.DAT",
        preprocessor="Prepro.exe",
        solver="Lagamine.exe",
        working_directory=directory,
    )
    return runner, lag_file, dat_file, preprocessor, solver


def test_preprocess_passes_correct_arguments_and_cwd(tmp_path, monkeypatch) -> None:
    runner, lag, _, prepro, _ = _make_inputs(tmp_path)
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    result = runner.preprocess(timeout=10, capture_output=True)
    assert result.stdout == "ok"
    cmd, options = calls[0]
    assert cmd == [str(prepro), str(lag), "x"]
    assert options["cwd"] == lag.parent
    assert options["timeout"] == 10
    assert options["check"] is True
    assert options["capture_output"] is True
    assert options["text"] is True


def test_solver_argument_order(tmp_path, monkeypatch) -> None:
    runner, lag, dat, _, exe = _make_inputs(tmp_path)
    dat.write_text("generated", encoding="utf-8")
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    runner.run()
    assert calls == [[str(exe), str(dat), str(lag), "x"]]


def test_only_selected_files_are_required(tmp_path, monkeypatch) -> None:
    runner, _, dat, _, _ = _make_inputs(tmp_path)

    def fake_run(command, **kwargs):
        return subprocess.CompletedProcess(command, returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert not dat.exists()
    runner.preprocess()  # DAT not required for preprocessing
    with pytest.raises(FileNotFoundError, match="dat_file"):
        runner.run()


def test_missing_executable_and_configuration(tmp_path) -> None:
    runner, _, dat, prepro, _ = _make_inputs(tmp_path)
    prepro.unlink()
    with pytest.raises(FileNotFoundError, match="executable for preprocessing"):
        runner.preprocess()
    runner.solver = None
    dat.write_text("ok", encoding="utf-8")
    with pytest.raises(ValueError, match="executable for solver"):
        runner.run()


def test_cwd_derived_from_nested_relative_lag_file(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    subdir = tmp_path / "nested"
    subdir.mkdir()
    (subdir / "model.LAG").write_text("model", encoding="utf-8")
    fake_exe = tmp_path / "Prepro.exe"
    fake_exe.write_text("executable", encoding="utf-8")
    runner = LagamineRunner(lag_file="nested/model.LAG", preprocessor=fake_exe)
    seen = []

    def fake_run(command, **kwargs):
        seen.append((command, kwargs["cwd"]))
        return subprocess.CompletedProcess(command, returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    runner.preprocess()
    assert seen == [([str(fake_exe), str(subdir / "model.LAG"), "x"], subdir)]


def test_failed_executable_propagates_error(tmp_path, monkeypatch) -> None:
    runner, lag, _, prepro, _ = _make_inputs(tmp_path)

    def fake_run(command, **kwargs):
        raise subprocess.CalledProcessError(12, command)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(subprocess.CalledProcessError) as info:
        runner.preprocess()
    assert info.value.returncode == 12


def test_timeout_propagates_without_swallowing(tmp_path, monkeypatch) -> None:
    runner, _, _, _, _ = _make_inputs(tmp_path)

    def fake_run(command, **kwargs):
        raise subprocess.TimeoutExpired(command, 0.01)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(subprocess.TimeoutExpired):
        runner.preprocess(timeout=0.01)


def test_batch_prepro_only_does_not_require_solver(tmp_path) -> None:
    runner, lag, dat, prepro, _ = _make_inputs(tmp_path)
    runner.solver = None
    runner.dat_file = None
    script = runner.write_batch_file(tmp_path / "prepro.bat", solve=False)
    content = script.read_text(encoding="utf-8")
    assert 'cd /d "' + str(lag.parent) + '"' in content
    assert f'"{prepro}" "{lag}" "x"' in content
    assert "Lagamine.exe" not in content
    assert content.count("if errorlevel 1") == 1
    assert not dat.exists()


def test_batch_solver_only_does_not_require_prepro(tmp_path) -> None:
    runner, lag, dat, _, exe = _make_inputs(tmp_path)
    runner.preprocessor = None
    script = runner.write_batch_file(tmp_path / "solver.bat", preprocess=False)
    text = script.read_text(encoding="utf-8")
    assert f'"{exe}" "{dat}" "{lag}" "x"' in text
    assert "Prepro.exe" not in text
    assert not dat.exists()  # can write a batch file before preparing DAT


def test_batch_rejects_malformed_argument(tmp_path) -> None:
    runner, _, _, _, _ = _make_inputs(tmp_path)
    runner.confirmation = '"& exit /b 0'
    with pytest.raises(ValueError, match="Batch arguments"):
        runner.write_batch_file(tmp_path / "bad.bat")


def test_batch_needs_one_stage(tmp_path) -> None:
    runner, _, _, _, _ = _make_inputs(tmp_path)
    with pytest.raises(ValueError, match="At least one"):
        runner.write_batch_file(tmp_path / "empty.bat", preprocess=False, solve=False)


@pytest.mark.skipif(os.name == "nt", reason="POSIX fake executable integration test")
def test_real_prepro_can_create_dat_before_solver(tmp_path) -> None:
    case = tmp_path / "newcase"
    case.mkdir()
    lag = case / "model.LAG"
    dat = case / "generated.DAT"
    lag.write_text("LAG file", encoding="utf-8")
    executable = tmp_path / "fake_lagamine"
    executable.write_text(
        '#!/usr/bin/env python3\n'
        'import pathlib, sys\n'
        'if len(sys.argv) == 3:\n'
        '    pathlib.Path("generated.DAT").write_text("created")\n'
        'elif len(sys.argv) == 4:\n'
        '    assert pathlib.Path(sys.argv[1]).read_text() == "created"\n'
        '    pathlib.Path("finished.txt").write_text("yes")\n'
        'else:\n'
        '    sys.exit(4)\n',
        encoding="utf-8",
    )
    executable.chmod(0o755)
    runner = LagamineRunner(
        lag_file=lag,
        dat_file=dat,
        preprocessor=executable,
        solver=executable,
    )
    first, second = runner.run_all(timeout=5)
    assert first.returncode == second.returncode == 0
    assert (case / "finished.txt").read_text(encoding="utf-8") == "yes"


def test_preprocessing_does_not_change_python_working_directory(tmp_path, monkeypatch) -> None:
    runner, _, _, _, _ = _make_inputs(tmp_path)
    original = Path.cwd()

    def fake_run(command, **kwargs):
        assert Path.cwd() == original
        return subprocess.CompletedProcess(command, returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    runner.preprocess()
    assert Path.cwd() == original


def test_run_all_does_not_start_solver_after_prepro_failure(tmp_path, monkeypatch) -> None:
    runner, _, _, _, _ = _make_inputs(tmp_path)
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        raise subprocess.CalledProcessError(2, command)

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(subprocess.CalledProcessError):
        runner.run_all()
    assert len(calls) == 1


def test_batch_percent_expansion_is_escaped(tmp_path) -> None:
    runner, _, _, _, _ = _make_inputs(tmp_path)
    runner.confirmation = "100%"
    script = runner.write_batch_file(tmp_path / "run.bat", solve=False)
    assert '"100%%"' in script.read_text(encoding="utf-8")
