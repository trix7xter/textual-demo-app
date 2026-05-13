from pathlib import Path

from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Tree
from textual.widgets._tree import TreeNode
from textual.message import Message

from note_app.repositories.base_folder_repository import BaseFolderRepository
from note_app.repositories.base_note_repository import BaseNoteRepository


class FileTreeWidget(VerticalScroll):
    _tree: Tree
    _folder_repo: BaseFolderRepository
    _root_path: Path

    class NoteSelected(Message):
        def __init__(self, note_path: Path):
            self.note_path = note_path
            super().__init__()

    class FolderSelected(Message):
        def __init__(self, folder_path: Path):
            self.folder_path = folder_path
            super().__init__()

    def __init__(
        self,
        folder_repo: BaseFolderRepository,
        note_repo: BaseNoteRepository,
        root_path: Path,
        *args,
        **kwargs,
    ) -> None:
        self._folder_repo = folder_repo
        self._note_repo = note_repo
        self._root_path = root_path
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        self._tree = Tree("Notices")
        yield self._tree

    def on_mount(self) -> None:
        root = self.query_one(Tree).root
        root.data = self._root_path
        root.expand()

    def reload(self) -> None:
        root = self.query_one(Tree).root
        root.collapse()
        root.expand()

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node: TreeNode[Path] = event.node
        if node.data is None:
            return
        node.remove_children()
        folders = self._folder_repo.get_folder_by_path(node.data)
        for folder in folders:
            node.add(folder.name, folder.path)
        notes = self._note_repo.get_notes_by_path(node.data)
        for note in notes:
            node.add_leaf(note.name, note.path)

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node: TreeNode[Path] = event.node
        if node.data and node.data.suffix == ".md":
            self.post_message(self.NoteSelected(node.data))

    def on_tree_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        node: TreeNode[Path] = event.node
        if node.data and not node.data.suffix == ".md":
            self.post_message(self.FolderSelected(node.data))
