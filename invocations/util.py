"""Utility functions used throughout the invocations package.
This module should not be added to any package invoke collections.
"""

from functools import reduce
import os
import subprocess
from pathlib import Path
from typing import Any
from glob import glob

from invoke import task, ParseError, Context


def _get_package_root():
    try:
        output = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
        output = output.decode().strip()
        return Path(output)
    except (FileNotFoundError, subprocess.SubprocessError):
        # handles the case where git is not installed correctly, but
        # assumes the invocations package is installed from root.
        return Path(__file__).parents[1].resolve()


REPO_ROOT = _get_package_root()


def remove_blank_lines(text):
    return os.linesep.join([s for s in text.splitlines() if s])


def safely_load_config(ctx: Context, config_path: str, default: Any = None) -> Any:
    """Tries to load a configuration item from the context provided,
    if it fails to find that configuration item, returns the default.

    The config path must be provided as a string using the same dot
    format expected when loading short-hand config items from
    the context. The leading 'ctx' can be ommitted.

    Example:

    .. code-block:: python

        config_foo_bar = safely_load_config(ctx, 'ctx.foo.bar', DEFAULT_FOO_BAR)
    """
    if not isinstance(ctx, Context):
        raise TypeError(f"ctx: expected Context instance, found {type(ctx)}")
    if not isinstance(config_path, str):
        raise TypeError(
            f"config_path: expected str instance, found {type(config_path)}"
        )
    if config_path[:1] == ".":
        config_path = config_path[1:]
    if config_path[:4] == "ctx.":
        config_path = config_path[4:]
    path_components = config_path.split(".")
    try:
        config_value = reduce(getattr, path_components, ctx)
        return config_value if config_value is not None else default
    except AttributeError:
        return default
