"""Command-line runner for externally installed Lagamine executables.

Only configured executable paths and input files are checked; optional
Lagamine companion files and generated result files are not guessed.
"""

import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

type PathInput = str | Path

_LOGGER = logging.getLogger(__name__)


@dataclass(slots=True, kw_only=True)
class LagamineRunner:
    """Configure and execute a Lagamine simulation from existing input files.

    Relative paths are interpreted from ``working_directory`` when it is
    specified, or from the directory containing ``lag_file`` otherwise.
    Without a specified ``working_directory``, a relative ``lag_file`` is
    interpreted from the Python process's current directory.

    ``dat_file`` may be the *expected* output of preprocessing: it is checked
    when the solver is launched, not when the runner is created. The optional
    token ``confirmation`` defaults to the ``x`` used by the provided scripts.

    Examples:
        >>> runner = LagamineRunner(lag_file="model.LAG")
        >>> # Supply preprocessor/solver paths before executing the model.
    """

    lag_file: PathInput
    dat_file: PathInput | None = None
    preprocessor: PathInput | None = None
    solver: PathInput | None = None
    working_directory: PathInput | None = None
    name: str | None = None
    comment: str | None = None
    confirmation: str = "x"

    def preprocess(
        self, *, timeout: float | None = None, capture_output: bool = False
    ) -> subprocess.CompletedProcess[str]:
        """Execute ``Prepro.exe <lag_file> <confirmation>``.

        Raises ``ValueError`` for unset inputs, ``FileNotFoundError`` for
        missing paths, ``subprocess.CalledProcessError`` for nonzero exit
        status, or ``subprocess.TimeoutExpired`` if a timeout is exceeded.
        """
        return self._execute_step(
            "preprocessing",
            executable=self.preprocessor,
            inputs=((self.lag_file, "lag_file"),),
            timeout=timeout,
            capture_output=capture_output,
        )

    def run(
        self, *, timeout: float | None = None, capture_output: bool = False
    ) -> subprocess.CompletedProcess[str]:
        """Execute ``Lagamine.exe <dat_file> <lag_file> <confirmation>``."""
        return self._execute_step(
            "solver",
            executable=self.solver,
            inputs=((self.dat_file, "dat_file"), (self.lag_file, "lag_file")),
            timeout=timeout,
            capture_output=capture_output,
        )

    def run_all(
        self, *, timeout: float | None = None, capture_output: bool = False
    ) -> tuple[subprocess.CompletedProcess[str], subprocess.CompletedProcess[str]]:
        """Run preprocessing then the solver, stopping if either step fails.

        ``timeout`` is applied **separately** to each executable. Set it to
        ``None`` to allow long simulations to finish without a time limit.
        """
        preprocessing = self.preprocess(timeout=timeout, capture_output=capture_output)
        simulation = self.run(timeout=timeout, capture_output=capture_output)
        return preprocessing, simulation

    def write_batch_file(
        self,
        output_path: PathInput,
        *,
        preprocess: bool = True,
        solve: bool = True,
    ) -> Path:
        """Write a Windows ``.bat`` script for the selected execution stages.

        Configured input/executable paths must be provided, but are not
        required to exist yet (the script may be generated before the files).
        The batch file stops at the first failed command and preserves its
        nonzero exit code. No file other than the selected inputs is checked.
        """
        if not (preprocess or solve):
            raise ValueError("At least one of preprocess or solve must be enabled")

        workdir = self._cwd()
        parts = ["@echo off", "setlocal DisableDelayedExpansion"]
        parts.append(f"cd /d {_batch_quote(workdir)} || exit /b 1")

        if preprocess:
            parts.extend(
                (
                    self._batch_command(
                        self.preprocessor,
                        "preprocessor",
                        ((self.lag_file, "lag_file"),),
                    ),
                    "if errorlevel 1 exit /b %errorlevel%",
                )
            )
        if solve:
            parts.extend(
                (
                    self._batch_command(
                        self.solver,
                        "solver",
                        ((self.dat_file, "dat_file"), (self.lag_file, "lag_file")),
                    ),
                    "if errorlevel 1 exit /b %errorlevel%",
                )
            )

        destination = Path(output_path).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\r\n".join(parts) + "\r\n", encoding="utf-8", newline="")
        _LOGGER.info("Wrote Lagamine batch file to %s", destination)
        return destination

    def _cwd(self) -> Path:
        if self.working_directory is not None:
            return Path(self.working_directory).expanduser().resolve()
        return Path(self.lag_file).expanduser().resolve().parent

    def _path(self, value: PathInput | None, label: str, *, check: bool) -> Path:
        if value is None:
            raise ValueError(f"{label} must be configured for this operation")
        path = Path(value).expanduser()
        if not path.is_absolute():
            # The implicit workdir is derived from lag_file; do not prefix
            # a relative lag_file twice (e.g. cases/model.LAG).
            if label == "lag_file" and self.working_directory is None:
                path = Path.cwd() / path
            else:
                path = self._cwd() / path
        path = path.resolve()
        if check and not path.is_file():
            raise FileNotFoundError(f"{label} does not exist or is not a file: {path}")
        return path

    def _execute_step(
        self,
        stage: Literal["preprocessing", "solver"],
        *,
        executable: PathInput | None,
        inputs: tuple[tuple[PathInput | None, str], ...],
        timeout: float | None,
        capture_output: bool,
    ) -> subprocess.CompletedProcess[str]:
        cwd = self._cwd()
        if not cwd.is_dir():
            raise NotADirectoryError(f"Working directory does not exist: {cwd}")

        executable_path = self._path(executable, "executable for " + stage, check=True)
        input_paths = [self._path(value, label, check=True) for value, label in inputs]
        command = [str(executable_path), *(str(path) for path in input_paths), self.confirmation]

        _LOGGER.info("Starting Lagamine %s in %s", stage, cwd)
        _LOGGER.debug("Command: %s", command)
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                check=True,
                timeout=timeout,
                capture_output=capture_output,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
            _LOGGER.exception("Lagamine %s failed", stage)
            raise
        _LOGGER.info("Lagamine %s completed (return code %s)", stage, result.returncode)
        return result

    def _batch_command(
        self,
        executable: PathInput | None,
        label: str,
        inputs: tuple[tuple[PathInput | None, str], ...],
    ) -> str:
        executable_path = self._path(executable, label, check=False)
        paths = [self._path(value, name, check=False) for value, name in inputs]
        return " ".join(
            [_batch_quote(executable_path), *(_batch_quote(path) for path in paths),
             _batch_quote(self.confirmation)]
        )


def _batch_quote(value: Path | str) -> str:
    """Quote a single Windows batch argument, escaping ``%`` expansion."""
    text = str(value)
    if not text or any(character in text for character in '\r\n"'):
        raise ValueError("Batch arguments cannot contain quotes or line breaks")
    return f'"{text.replace("%", "%%")}"'
