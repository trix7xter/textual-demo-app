from pathlib import Path
import shutil

from note_app.domain.folder import Folder
from note_app.repositories.base_folder_repository import BaseFolderRepository


class FolderRepository(BaseFolderRepository):
    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path

    def _check_within_base(self, path: Path) -> None:
        if self.base_path not in path.parents and path != self.base_path:
            raise ValueError("Access outside data directory is not allowed")

    def get_folder_by_path(self, path: Path) -> list[Folder]:
        path = path.resolve()
        self._check_within_base(path)
        if not path.is_dir():
            raise ValueError(f"Folder doesn't exist: {path}")

        folders: list[Folder] = []
        for sub_path in path.iterdir():
            if sub_path.is_dir() and not sub_path.name.startswith("."):
                folders.append(Folder(name=sub_path.name, path=sub_path))

        return sorted(folders, key=lambda f: f.name)

    def create_folder(self, path: Path, name: str) -> Folder:
        path = path.resolve()
        self._check_within_base(path)
        if not path.is_dir():
            raise ValueError(f"Parent folder doesn't exist: {path}")
        if not name or "/" in name or "\\" in name:
            raise ValueError("Invalid folder name")

        new_path = path / name
        new_path.mkdir(exist_ok=False)
        return Folder(name, new_path)

    def delete_folder(self, folder: Folder) -> None:
        path = folder.path.resolve()
        self._check_within_base(path)
        if not path.is_dir():
            raise ValueError(f"Folder doesn't exist: {path}")
        if path == self.base_path:
            raise ValueError("Cannot delete base path")

        shutil.rmtree(path)
