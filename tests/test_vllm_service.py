"""Unit tests for the VLLMService."""

from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from requests.exceptions import RequestException

from src.photo_search.vllm_service import VLLMService


@patch("src.photo_search.vllm_service.get_settings")
def test_get_description_success(mock_get_settings):
    """Test successfully getting a description from the VLLM."""
    # Arrange
    mock_settings = MagicMock()
    mock_settings.vllm_api_key = "test_key"
    mock_settings.vllm_api_endpoint = "http://fake-url.com/invocations"
    mock_get_settings.return_value = mock_settings

    with patch("src.photo_search.vllm_service.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"predictions": ["A beautiful landscape."]}
        mock_post.return_value = mock_response

        service = VLLMService()
        fake_image_path = Path("fake_image.jpg")

        # Act
        with patch("builtins.open", MagicMock()):
            with patch("base64.b64encode", return_value=b"encoded_string") as mock_b64encode:
                description = service.get_description(fake_image_path)

    # Assert
    assert description == "A beautiful landscape."
    mock_b64encode.assert_called_once()
    mock_post.assert_called_once_with(
        "http://fake-url.com/invocations",
        json={"instances": [{"image_bytes": {"b64": "encoded_string"}}]},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer test_key",
        },
        timeout=30,
    )


@patch("src.photo_search.vllm_service.get_settings")
def test_get_description_io_error(mock_get_settings):
    """Test that an IOError is raised when the image file cannot be read."""
    # Arrange
    mock_settings = MagicMock()
    mock_settings.vllm_api_key = "test_key"
    mock_settings.vllm_api_endpoint = "http://fake-url.com/invocations"
    mock_get_settings.return_value = mock_settings

    service = VLLMService()
    fake_image_path = Path("non_existent_image.jpg")

    # Act & Assert
    with patch("builtins.open", side_effect=IOError("File not found")):
        with pytest.raises(IOError, match="Could not read image file"):
            service.get_description(fake_image_path)


@patch("src.photo_search.vllm_service.get_settings")
def test_get_description_request_exception(mock_get_settings):
    """Test that a RequestException is raised on API failure."""
    # Arrange
    mock_settings = MagicMock()
    mock_settings.vllm_api_key = "test_key"
    mock_settings.vllm_api_endpoint = "http://fake-url.com/invocations"
    mock_get_settings.return_value = mock_settings

    with patch("src.photo_search.vllm_service.requests.post") as mock_post:
        mock_post.side_effect = RequestException("API is down")

        service = VLLMService()
        fake_image_path = Path("fake_image.jpg")

        # Act & Assert
        with patch("builtins.open", MagicMock()):
            with patch("base64.b64encode", return_value=b"encoded_string"):
                with pytest.raises(RequestException, match="Failed to get description from VLLM"):
                    service.get_description(fake_image_path) 