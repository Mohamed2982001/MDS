"""
Master Design System (MDS) -- CI Provider Adapters Package
"""

import os
from pathlib import Path

from .base import CIProviderAdapter
from .github import GitHubActionsAdapter
from .gitlab import GitLabCIAdapter
from .local import LocalRunnerAdapter


def detect_adapter(workspace_root: Path, force_provider: str = "") -> CIProviderAdapter:
    """
    Factory resolving the appropriate CIProviderAdapter based on environment variables.
    """
    if force_provider == "github_actions" or os.environ.get("GITHUB_ACTIONS") == "true":
        return GitHubActionsAdapter(workspace_root)
    if force_provider == "gitlab_ci" or os.environ.get("GITLAB_CI") == "true":
        return GitLabCIAdapter(workspace_root)
    return LocalRunnerAdapter(workspace_root)


__all__ = [
    "CIProviderAdapter",
    "GitHubActionsAdapter",
    "GitLabCIAdapter",
    "LocalRunnerAdapter",
    "detect_adapter",
]
