"""Database management for the photo search application."""

import os
from pathlib import Path
from typing import List, Optional

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    select,
    insert,
    update,
)

from src.photo_search.photos_service import PhotoInfo

DEFAULT_DB_PATH = Path.home() / ".photo_search" / "photos.db"


class Database:
    """Handles all database interactions for the photo search application."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH) -> None:
        """Initialize the database.

        Args:
            db_path: The path to the SQLite database file.
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        self.metadata = MetaData()
        self.photos = Table(
            "photos",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("uuid", String, unique=True, nullable=False),
            Column("filepath", String, nullable=False),
            Column("description", String),
        )

    def create_database(self) -> None:
        """Create the database and tables if they don't exist."""
        self.metadata.create_all(self.engine)

    def is_photo_indexed(self, photo_uuid: str) -> bool:
        """Check if a photo has already been indexed.

        Args:
            photo_uuid: The UUID of the photo to check.

        Returns:
            True if the photo is indexed, False otherwise.
        """
        with self.engine.connect() as connection:
            stmt = select(self.photos).where(self.photos.c.uuid == photo_uuid)
            result = connection.execute(stmt).first()
            return result is not None

    def add_photo(self, photo: PhotoInfo, description: str) -> None:
        """Add or update a photo's description in the database.

        Args:
            photo: The PhotoInfo object.
            description: The description of the photo.
        """
        with self.engine.connect() as connection:
            if self.is_photo_indexed(photo.uuid):
                stmt = (
                    update(self.photos)
                    .where(self.photos.c.uuid == photo.uuid)
                    .values(description=description)
                )
            else:
                stmt = insert(self.photos).values(
                    uuid=photo.uuid,
                    filepath=str(photo.path),
                    description=description,
                )
            connection.execute(stmt)
            connection.commit()

    def search_photos(self, query: str) -> List[str]:
        """Search for photos by matching the query against their descriptions.

        Args:
            query: The natural language search query.

        Returns:
            A list of file paths for the matching photos.
        """
        # A simple LIKE query for now. This will be improved with more
        # sophisticated semantic search later.
        with self.engine.connect() as connection:
            stmt = select(self.photos.c.filepath).where(
                self.photos.c.description.like(f"%{query}%")
            )
            results = connection.execute(stmt).fetchall()
            return [row[0] for row in results] 