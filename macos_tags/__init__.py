"""A python libraty for working with macOS tags"""
import sys

from ._api import *


def _test_os() -> None:
    """Raise an error if it's not MacOS."""
    if sys.platform != "darwin":
        raise RuntimeError(f"The library works only on macOS.")


_test_os()
