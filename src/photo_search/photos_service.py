"""Service for interacting with the Apple Photos library."""

from typing import List, NamedTuple, Optional

import osxphotos


class PhotoInfo(NamedTuple):
    """A named tuple to hold information about a photo."""

    uuid: str
    path: str


class PhotosService:
    """A service to interact with the Apple Photos library."""

    def __init__(self, db_path: Optional[str] = None) -> None:
        """Initialize the PhotosService.

        Args:
            db_path: Optional path to the Photos library database.
                     If None, osxphotos will try to find the default library.

        Raises:
            FileNotFoundError: If the Photos database cannot be found.

        """
        try:
            self.photos_db = osxphotos.PhotosDB(dbfile=db_path)
        except FileNotFoundError:
            # Re-raise the exception to be handled by the caller
            raise

    def get_photos(self) -> List[PhotoInfo]:
        """Fetch a list of photos from the Apple Photos library.

        Returns:
            A list of PhotoInfo objects, each containing the UUID and path of a photo.
            Returns an empty list if there are no photos or the path is not available.

        """
        photo_infos: List[PhotoInfo] = []
        # photos() returns a list of PhotoInfo objects from osxphotos
        for photo in self.photos_db.photos():
            # Only include photos that have a path on the local disk
            if photo.path:
                photo_infos.append(PhotoInfo(uuid=photo.uuid, path=photo.path))
        return photo_infos
