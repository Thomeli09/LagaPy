"""LagaPy: Python tools for preparing and executing Lagamine simulations.

The core FE model, file readers, result analysis and plotting are still under
active development. Importing LagaPy never starts an external executable.
"""

import logging
from importlib.metadata import PackageNotFoundError, version

# Recommended library practice: remain silent unless an application configures
# logging explicitly, without altering the process-wide root logger.
logging.getLogger(__name__).addHandler(logging.NullHandler())

try:
    __version__ = version("lagapy")
except PackageNotFoundError:
    __version__ = "0+unknown"

__all__ = ["__version__"]
