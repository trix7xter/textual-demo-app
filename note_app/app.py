from textual.app import App

from note_app.config.config import AppSettings
from note_app.repositories.folder_repository import FolderRepository
from note_app.repositories.note_repository import NoteRepository
from note_app.screens.main import MainScreen


class NoteManagerApp(App):
    def __init__(self, settings: AppSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings

    def on_mount(self) -> None:
        folder_repo = FolderRepository(self.settings.data_directory)
        note_repo = NoteRepository(self.settings.data_directory)
        main_screen = MainScreen(self.settings, folder_repo, note_repo)
        self.push_screen(main_screen)
