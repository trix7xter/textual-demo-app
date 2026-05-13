from datetime import datetime
from typing import Optional

import html2text
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header
from textual.containers import Horizontal

from note_app.config.config import AppSettings
from note_app.domain.note import Note
from note_app.screens.import_modal import ImportModal
from note_app.widgets.file_tree import FileTreeWidget
from note_app.widgets.note_view import NoteViewWidget

from note_app.repositories.base_folder_repository import BaseFolderRepository
from note_app.repositories.base_note_repository import BaseNoteRepository


class MainScreen(Screen):
    CSS = """
    #tree {
        width: 25%
    }
    """
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("i", "import", "Import"),
        ("d", "delete", "Delete"),
    ]

    def __init__(
        self,
        settings: AppSettings,
        folder_repo: BaseFolderRepository,
        note_repo: BaseNoteRepository,
        *args,
        **kwargs,
    ) -> None:
        self._folder_repo = folder_repo
        self._note_repo = note_repo
        self._dir = settings.data_directory
        self._note: Note | None = None
        self.settings = settings
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield FileTreeWidget(
                self._folder_repo, self._note_repo, self.settings.data_directory
            )
            yield NoteViewWidget()
        yield Footer()

    def on_mount(self) -> None:
        self.title = self.settings.app_name
        self.query_one(NoteViewWidget).text = "## Hello"

    def action_import(self) -> None:
        self.app.push_screen(ImportModal(), self.handle_import)

    def handle_import(self, data: Optional[str]) -> None:
        if not data:
            return
        md = html2text.html2text(data)
        name = f"imported_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            self._note_repo.create_note(self._dir, name, md)
        except (OSError, ValueError) as e:
            self.app.notify(f"Import error: {e}", severity="error")
            return
        self.query_one(FileTreeWidget).reload()

    def action_quit(self) -> None:
        self.app.exit()

    def action_delete(self) -> None:
        if self._note is None:
            return
        try:
            self._note_repo.delete_note(self._note)
        except (OSError, ValueError) as e:
            self.app.notify(f"Delete error: {e}", severity="error")
            return
        self._note = None
        self.query_one(NoteViewWidget).text = ""
        self.query_one(FileTreeWidget).reload()

    def on_file_tree_widget_note_selected(
        self, message: FileTreeWidget.NoteSelected
    ) -> None:
        note = self._note_repo.load_note(message.note_path)
        self._note = note
        if note.content:
            self.query_one(NoteViewWidget).text = note.content
        else:
            self.query_one(NoteViewWidget).text = ""

    def on_file_tree_widget_folder_selected(
        self, message: FileTreeWidget.FolderSelected
    ) -> None:
        self._dir = message.folder_path
