"""Configuration management for the photo search application.

This module loads settings from environment variables and a .env file.
"""

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from a .env file located in the project root.
# The project root is determined by looking for the pyproject.toml file.
def get_project_root() -> Path:
    """Find the project root by locating the 'pyproject.toml' file.

    Raises:
        FileNotFoundError: If 'pyproject.toml' is not found in parent directories.

    """
    current_path = Path.cwd()
    while current_path != current_path.parent:
        if (current_path / "pyproject.toml").exists():
            return current_path
        current_path = current_path.parent
    raise FileNotFoundError("Project root with 'pyproject.toml' not found.")

project_root = get_project_root()
dotenv_path = project_root / ".env"
load_dotenv(dotenv_path=dotenv_path)


class Settings:
    """Application settings loaded from environment variables."""

    vllm_api_key: str
    vllm_api_endpoint: str

    def __init__(self) -> None:
        """Initialize settings, loading from environment variables."""
        api_key = os.getenv("VLLM_API_KEY")
        if not api_key:
            raise ValueError("VLLM_API_KEY environment variable not set.")
        self.vllm_api_key = api_key

        api_endpoint = os.getenv("VLLM_API_ENDPOINT")
        if not api_endpoint:
            raise ValueError("VLLM_API_ENDPOINT environment variable not set.")
        self.vllm_api_endpoint = api_endpoint


@lru_cache()
def get_settings() -> Settings:
    """Get the application settings.

    This function is cached to ensure that the settings are loaded only once.
    It also loads environment variables from a .env file.

    Returns:
        The application settings object.

    """
    project_root = get_project_root()
    dotenv_path = project_root / ".env"
    load_dotenv(dotenv_path=dotenv_path)
    return Settings()
