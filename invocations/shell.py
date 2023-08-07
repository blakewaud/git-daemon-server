import os
import platform
from pathlib import Path
import re
from typing import Optional
from colorama import Fore, Style
from invoke import Context

from invocations.errors import WrongBranchError
from invocations.util import (
    REPO_ROOT,
    remove_blank_lines,
    safely_load_config,
)

POETRY = "poetry"
PIP = "pip"
SPHINX = "sphinx-build"
DOCGEN = "docgen"
PYTHON_EXECUTOR = "python"
INVOKE = "invoke"
GIT = "git"
WSL = "wsl"
POWERSHELL = "pwsh -c"

SEMANTIC_VERSION_PATTERN = re.compile(
    r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(\-((0|[1-9A-Za-z-]+)((\.(0|[1-9A-Za-z-]+))+)?))?(\+(([0-9A-Za-z-]+)((\.([0-9A-Za-z-]+))+)?))?"  # noqa
)

if platform.system() != "Windows":
    REL_ACTIVATE_PATH = Path(".venv") / "bin" / "activate"
    ACTIVATE_TEMPLATE = "source {}"
else:
    REL_ACTIVATE_PATH = Path(".venv") / "Scripts" / "activate"
    ACTIVATE_TEMPLATE = "{}.bat"


def get_venv_activate_cmd(ctx: Context) -> str:
    """Determines and returns the path to the package's .venv
    activation scripts based on the context passed in.
    """
    if safely_load_config(ctx, "is_meta"):
        abs_activate_path = REPO_ROOT / REL_ACTIVATE_PATH
    else:
        abs_activate_path = (
            Path(safely_load_config(ctx, "package_dir")) / REL_ACTIVATE_PATH
        )
    return ACTIVATE_TEMPLATE.format(abs_activate_path.resolve())


def run(ctx: Context, app: str, command: str, **kwargs):
    """Generic run command for any shell executables"""
    return ctx.run(f"{app} {command}", **kwargs)


def powershell(ctx, command: str, **kwargs):
    """Executes a powershell command on the shell"""
    return run(ctx, POWERSHELL, command, **kwargs)


def poetry(ctx: Context, command: str, **kwargs):
    """Executes poetry commands on the shell."""
    return run(ctx, POETRY, f"{command}", **kwargs)


def run_in_venv(ctx: Context, app: str, command: str, **kwargs):
    """Execute a command within the poetry venv using
    ``poetry run``
    """
    return poetry(ctx, f"run {app} {command}", **kwargs)


def pip(ctx: Context, command: str, **kwargs):
    """Execute a pip command on the shell"""
    return run(ctx, PIP, command, **kwargs)


def git(ctx: Context, command: str, **kwargs):
    """Executes a git command on the shell"""
    return run(ctx, GIT, command, **kwargs)


def invoke(ctx: Context, command: str, **kwargs):
    """Executes an invoke command within the current context."""
    return run(ctx, INVOKE, command, **kwargs)


def wsl(ctx: Context, command: str, **kwargs):
    """Executes a command within the WSL environment."""
    return run(ctx, WSL, command, **kwargs)


def require_git_branch(ctx: Context, expected_branch: Optional[str] = None) -> None:
    """Checks if the current git branch matched the ``expected_branch``,
    which defaults to the ``main`` branch. You can also set this via
    context config item ``main_branch_name``.
    """
    if expected_branch is None:
        main_branch_name = safely_load_config(ctx, "ctx.main_branch_name", "main")
    else:
        main_branch_name = expected_branch
    branch = git(
        ctx, "rev-parse --abbrev-ref HEAD", echo=False, hide=True
    ).stdout.strip()
    if branch != main_branch_name:
        raise WrongBranchError(branch, main_branch_name)
