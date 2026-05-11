from textual.app import ComposeResult
from textual.events import Mount
from textual.screen import Screen
from textual.widgets import Footer, Header
from textual.containers import Horizontal

from note_app.config.config import AppSettings
from note_app.repositories.folder_repository import FolderRepository
from note_app.widgets.file_tree import FileTreeWidget
from note_app.widgets.note_view import NoteViewWidget


class MainScreen(Screen):
    CSS = """
    #tree {
        width: 25%
    }
    """
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self, settings: AppSettings, *args, **kwargs) -> None:
        self.settings = settings
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        folder_repo = FolderRepository(self.settings.data_directory)
        yield Header()
        with Horizontal():
            yield FileTreeWidget(folder_repo, self.settings.data_directory)
            yield NoteViewWidget()
        yield Footer()

    def _on_mount(self, event: Mount) -> None:
        self.title = "Notice Manager"
        self.query_one(NoteViewWidget).text = "## Hello"
        return super()._on_mount(event)

    def action_quit(self):
        self.app.exit()
