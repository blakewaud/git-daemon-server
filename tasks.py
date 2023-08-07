from typing import Optional

from invoke.tasks import task
from invoke.context import Context

from invocations import util, shell


@task
def start_daemon(ctx: Context, receive: Optional[bool] = None):
    """Starts the Git daemon.

    Args:
        receive (bool): Whether to allow receiving of pushes from clients.
    """
    if receive is None:
        receive = util.safely_load_config(ctx, "git_daemon.receive", True)
    receive_str = "--enable=receive-pack" if receive else ""
    shell.git(
        ctx,
        f"daemon --reuseaddr --verbose "
        f"--base-path={util.safely_load_config(ctx, 'git_daemon.base_path', '.')} "
        f"--export-all {receive_str} ",
    )


@task
def clean(ctx: Context):
    """Cleans the project."""
    shell.git(ctx, "clean -fdx")


@task
def install_wsl_env(ctx: Context):
    """Installs the WSL environment for the project."""
    shell.wsl(ctx, "python -m poetry install")
