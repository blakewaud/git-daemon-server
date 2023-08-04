import yaml
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
