"""Service for interacting with the external VLLM."""

import base64
from pathlib import Path

import requests
from requests.exceptions import RequestException
from src.photo_search.config import get_settings


class VLLMService:
    """A service to interact with a VLLM to get image descriptions."""

    def __init__(self) -> None:
        """Initialize the VLLMService."""
        settings = get_settings()
        self.api_key = settings.vllm_api_key
        self.api_endpoint = settings.vllm_api_endpoint

    def get_description(self, image_path: Path) -> str:
        """Get a description for an image from the VLLM.

        Args:
            image_path: The path to the image file.

        Returns:
            A string containing the description of the image.

        Raises:
            IOError: If the image file cannot be read.
            RequestException: If the request to the VLLM fails.

        """
        if not self.api_endpoint:
            raise ValueError("VLLM API endpoint is not configured.")

        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            raise IOError(f"Could not read image file: {image_path}") from e

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {"instances": [{"image_bytes": {"b64": encoded_image}}]}

        try:
            response = requests.post(
                self.api_endpoint, json=payload, headers=headers, timeout=30
            )
            response.raise_for_status()
            # Assuming the response has a 'predictions' field
            return response.json()["predictions"][0]
        except RequestException as e:
            raise RequestException(f"Failed to get description from VLLM: {e}") from e
