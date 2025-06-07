"""Unit tests for the PhotosService."""

import pytest
from unittest.mock import MagicMock, patch

from src.photo_search.photos_service import PhotosService, PhotoInfo


@patch("src.photo_search.photos_service.osxphotos.PhotosDB")
def test_get_photos_success(mock_photos_db_class):
    """Test successfully fetching photos."""
    # Arrange
    mock_photo_1 = MagicMock()
    mock_photo_1.uuid = "uuid1"
    mock_photo_1.path = "/path/to/photo1.jpg"

    mock_photo_2 = MagicMock()
    mock_photo_2.uuid = "uuid2"
    mock_photo_2.path = "/path/to/photo2.jpg"

    mock_photo_3_no_path = MagicMock()
    mock_photo_3_no_path.uuid = "uuid3"
    mock_photo_3_no_path.path = None

    mock_db_instance = MagicMock()
    mock_db_instance.photos.return_value = [mock_photo_1, mock_photo_2, mock_photo_3_no_path]
    mock_photos_db_class.return_value = mock_db_instance

    # Act
    service = PhotosService()
    photos = service.get_photos()

    # Assert
    assert photos == [
        PhotoInfo(uuid="uuid1", path="/path/to/photo1.jpg"),
        PhotoInfo(uuid="uuid2", path="/path/to/photo2.jpg"),
    ]
    mock_photos_db_class.assert_called_once_with(dbfile=None)
    mock_db_instance.photos.assert_called_once()


@patch("src.photo_search.photos_service.osxphotos.PhotosDB")
def test_get_photos_empty(mock_photos_db_class):
    """Test fetching photos when the library is empty."""
    # Arrange
    mock_db_instance = MagicMock()
    mock_db_instance.photos.return_value = []
    mock_photos_db_class.return_value = mock_db_instance

    # Act
    service = PhotosService()
    photos = service.get_photos()

    # Assert
    assert photos == []


@patch("src.photo_search.photos_service.osxphotos.PhotosDB")
def test_photos_service_init_raises_file_not_found(mock_photos_db_class):
    """Test that PhotosService raises FileNotFoundError if the DB is not found."""
    # Arrange
    mock_photos_db_class.side_effect = FileNotFoundError("DB not found")

    # Act & Assert
    with pytest.raises(FileNotFoundError, match="DB not found"):
        PhotosService() 