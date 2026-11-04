"""Example CLI for launching existing Lagamine files (no files are generated).

Run ``python examples/run_lagamine.py --help`` for required arguments.
"""

import argparse
import logging
from pathlib import Path

from lagapy.logging import configure_logging
from lagapy.solver import LagamineRunner


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lag", type=Path, required=True, help="Input .LAG file")
    parser.add_argument("--dat", type=Path, help="Input/expected generated .DAT file")
    parser.add_argument("--prepro", type=Path, help="Path to Prepro.exe")
    parser.add_argument("--lagamine", type=Path, help="Path to Lagamine.exe")
    parser.add_argument("--workdir", type=Path, help="Directory where executables run")
    parser.add_argument("--log-file", type=Path, help="Optional rotating LagaPy log")
    levels = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    parser.add_argument("--console-level", choices=levels, default="INFO")
    parser.add_argument("--file-level", choices=levels, default="DEBUG")
    parser.add_argument("--no-console", action="store_true", help="Disable Python console logs")
    parser.add_argument("--timeout", type=float, default=None, help="Limit per stage in seconds")
    parser.add_argument("--preprocess-only", action="store_true")
    parser.add_argument("--solve-only", action="store_true")
    parser.add_argument("--batch", type=Path, help="Generate a Windows batch file, do not run")
    args = parser.parse_args()
    if args.preprocess_only and args.solve_only:
        parser.error("--preprocess-only and --solve-only are mutually exclusive")

    configure_logging(
        output=args.log_file,
        console_level=None if args.no_console else getattr(logging, args.console_level),
        file_level=getattr(logging, args.file_level),
    )
    runner = LagamineRunner(
        lag_file=args.lag,
        dat_file=args.dat,
        preprocessor=args.prepro,
        solver=args.lagamine,
        working_directory=args.workdir,
    )
    do_preprocess = not args.solve_only
    do_solve = not args.preprocess_only

    if args.batch is not None:
        runner.write_batch_file(args.batch, preprocess=do_preprocess, solve=do_solve)
    elif do_preprocess and do_solve:
        runner.run_all(timeout=args.timeout)
    elif do_preprocess:
        runner.preprocess(timeout=args.timeout)
    else:
        runner.run(timeout=args.timeout)


if __name__ == "__main__":
    main()
