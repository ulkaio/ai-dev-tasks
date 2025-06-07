"""Unit tests for the Database class."""

from pathlib import Path
import pytest
from sqlalchemy import create_engine, inspect

from src.photo_search.database import Database
from src.photo_search.photos_service import PhotoInfo


@pytest.fixture
def in_memory_db() -> Database:
    """Fixture to create an in-memory SQLite database for testing."""
    db = Database(db_path=Path(":memory:"))
    db.create_database()
    return db


def test_create_database(in_memory_db: Database):
    """Test that the database and 'photos' table are created."""
    inspector = inspect(in_memory_db.engine)
    assert "photos" in inspector.get_table_names()
    columns = [col["name"] for col in inspector.get_columns("photos")]
    assert "id" in columns
    assert "uuid" in columns
    assert "filepath" in columns
    assert "description" in columns


def test_add_and_check_photo(in_memory_db: Database):
    """Test adding a photo and checking if it's indexed."""
    # Arrange
    photo = PhotoInfo(uuid="uuid1", path="/path/to/photo1.jpg")
    description = "A test photo."

    # Act
    assert not in_memory_db.is_photo_indexed("uuid1")
    in_memory_db.add_photo(photo, description)

    # Assert
    assert in_memory_db.is_photo_indexed("uuid1")


def test_update_photo(in_memory_db: Database):
    """Test updating an existing photo's description."""
    # Arrange
    photo = PhotoInfo(uuid="uuid1", path="/path/to/photo1.jpg")
    initial_description = "Initial description."
    updated_description = "Updated description."

    in_memory_db.add_photo(photo, initial_description)

    # Act
    in_memory_db.add_photo(photo, updated_description)

    # Assert
    # Check that the description was updated
    with in_memory_db.engine.connect() as connection:
        result = connection.execute(
            in_memory_db.photos.select().where(in_memory_db.photos.c.uuid == "uuid1")
        ).first()
        assert result is not None
        assert result.description == updated_description


def test_search_photos(in_memory_db: Database):
    """Test searching for photos."""
    # Arrange
    photo1 = PhotoInfo(uuid="uuid1", path="/path/to/cat.jpg")
    desc1 = "A photo of a black cat."
    photo2 = PhotoInfo(uuid="uuid2", path="/path/to/dog.jpg")
    desc2 = "A photo of a golden dog."
    photo3 = PhotoInfo(uuid="uuid3", path="/path/to/another_cat.jpg")
    desc3 = "A playful white cat."

    in_memory_db.add_photo(photo1, desc1)
    in_memory_db.add_photo(photo2, desc2)
    in_memory_db.add_photo(photo3, desc3)

    # Act
    cat_results = in_memory_db.search_photos("cat")
    dog_results = in_memory_db.search_photos("dog")
    non_existent_results = in_memory_db.search_photos("bird")

    # Assert
    assert len(cat_results) == 2
    assert "/path/to/cat.jpg" in cat_results
    assert "/path/to/another_cat.jpg" in cat_results
    assert len(dog_results) == 1
    assert "/path/to/dog.jpg" in dog_results
    assert len(non_existent_results) == 0 