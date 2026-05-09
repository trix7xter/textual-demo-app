from textual.app import ComposeResult
from textual.events import Mount
from textual.screen import Screen
from textual.widgets import Footer, Header, Tree, Markdown
from textual.containers import Horizontal

from note_app.widgets.markdown import MarkdownWidget


class MainScreen(Screen):
    CSS = """
    #tree {
        width: 25%
    }
    """
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield Tree(label="My database", id="tree")
            yield MarkdownWidget()
        yield Footer()

    def _on_mount(self, event: Mount) -> None:
        self.title = "Notice Manager"
        self.query_one(MarkdownWidget).text = "## Hello"
        return super()._on_mount(event)

    def action_quit(self):
        self.app.exit()
