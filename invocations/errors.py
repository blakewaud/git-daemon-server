"""Custom error types used by the invocations package"""
from typing import Optional
from invoke import Context


class RpaInvokeError(Exception):
    """Unspecified error from rpaframework invocations."""

    pass


class WrongBranchError(RpaInvokeError):
    """Raised when an operation is attempted on the incorrect git
    branch.
    """

    def __init__(
        self,
        current_branch: str,
        expected_branch: str,
        context: Optional[Context] = None,
    ) -> None:
        self.current_branch = current_branch
        self.expected_branch = expected_branch
        self.message = f"On branch '{self.current_branch}' but expected branch '{self.expected_branch}'"
        self.ctx = context
        super().__init__(self.message)
