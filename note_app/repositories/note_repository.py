from pathlib import Path
from typing import Optional

from note_app.domain.note import Note
from note_app.repositories.base_note_repository import BaseNoteRepository


class NoteRepository(BaseNoteRepository):
    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path.resolve()

    def _check_within_base(self, path: Path) -> None:
        if self.base_path not in path.parents and path != self.base_path:
            raise ValueError("Access outside data directory is not allowed")

    def get_notes_by_path(self, path: Path) -> list[Note]:
        path = path.resolve()
        self._check_within_base(path)
        if not path.is_dir():
            raise ValueError(f"Folder doesn't exist: {path}")

        notes: list[Note] = []
        for sub_path in path.iterdir():
            if (
                sub_path.is_file()
                and not sub_path.name.startswith(".")
                and sub_path.suffix == ".md"
            ):
                notes.append(Note(sub_path.stem, sub_path))

        return sorted(notes, key=lambda n: n.name)

    def create_note(self, path: Path, name: str, content: str) -> Note:
        path = path.resolve()
        self._check_within_base(path)
        if not path.is_dir():
            raise ValueError(f"Folder doesn't exist: {path}")
        if not name or "/" in name or "\\" in name:
            raise ValueError("Invalid note name")

        note_path = path / f"{name}.md"
        if note_path.exists():
            raise ValueError(f"Note already exists: {note_path}")
        note_path.write_text(content, encoding="utf-8")
        return Note(name, note_path)

    def update_note(self, note: Note, content: str, new_name: Optional[str]) -> Note:
        path = note.path.resolve()
        self._check_within_base(path)
        if not path.is_file():
            raise ValueError(f"Note doesn't exist: {path}")

        if new_name and new_name != note.name:
            if "/" in new_name or "\\" in new_name:
                raise ValueError("Invalid note name")
            new_path = (path.parent / f"{new_name}.md").resolve()
            self._check_within_base(new_path)
            if new_path.exists():
                raise ValueError(f"Note already exists: {new_path}")
            path.write_text(content, encoding="utf-8")
            path.rename(new_path)
            return Note(new_name, new_path, content=content)

        path.write_text(content, encoding="utf-8")
        return Note(note.name, path, content=content)

    def delete_note(self, note: Note) -> None:
        path = note.path.resolve()
        self._check_within_base(path)
        if not path.is_file():
            raise ValueError(f"Note doesn't exist: {path}")
        path.unlink()

    def load_note(self, path: Path) -> Note:
        path = path.resolve()
        self._check_within_base(path)
        if not path.is_file():
            raise ValueError(f"Note doesn't exist: {path}")
        content = path.read_text(encoding="utf-8")
        return Note(path.stem, path, content)
